"""
MCP Orchestrator
─────────────────────────────────────────────────────────────────────────────
Connects to all MCP servers, discovers tools, and uses an LLM (Groq, Gemini,
or Ollama) to plan and execute tool calls step-by-step until the user goal
is achieved.

Key design choices
  • Tool discovery is automatic — the LLM sees all tools across all servers.
  • The LLM decides the order of calls; nothing is hard-coded.
  • Each call is logged (inputs + output summary, no secrets).
  • Failures trigger a retry with exponential back-off, then a fallback.
  • Yields events (dicts) so the UI can stream live updates.
"""

import asyncio
import json
import logging
import os
import sys
import time
from contextlib import asynccontextmanager
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator

import httpx
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

# ── Logging ───────────────────────────────────────────────────────────────────

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE  = os.getenv("LOG_FILE",  "./logs/scout.log")
Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stderr),
    ],
)
logger = logging.getLogger("orchestrator")

# ── Config ────────────────────────────────────────────────────────────────────

LLM_BACKEND     = os.getenv("LLM_BACKEND",     "groq").lower()
GROQ_API_KEY    = os.getenv("GROQ_API_KEY",    "")
GROQ_MODEL      = os.getenv("GROQ_MODEL",      "llama-3.3-70b-versatile")
GEMINI_API_KEY  = os.getenv("GEMINI_API_KEY",  "")
GEMINI_MODEL    = os.getenv("GEMINI_MODEL",    "gemini-2.0-flash")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL",    "llama3")
BRAVE_API_KEY   = os.getenv("BRAVE_API_KEY",   "")
OUTPUT_DIR      = Path(os.getenv("OUTPUT_DIR", "./outputs"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MAX_STEPS        = 12
RETRY_ATTEMPTS   = 3
RETRY_BASE_DELAY = 1.5   # seconds


# ── MCP server configurations ─────────────────────────────────────────────────

def get_server_configs() -> list[dict]:
    configs = []

    # 1. Brave Search (third-party)
    if BRAVE_API_KEY:
        configs.append({
            "name": "brave-search",
            "params": StdioServerParameters(
                command="npx",
                args=["-y", "@modelcontextprotocol/server-brave-search"],
                env={"BRAVE_API_KEY": BRAVE_API_KEY},
            ),
        })
    else:
        logger.warning("BRAVE_API_KEY not set — brave-search server will be skipped")

    # 2. Filesystem (third-party)
    configs.append({
        "name": "filesystem",
        "params": StdioServerParameters(
            command="npx",
            args=[
                "-y",
                "@modelcontextprotocol/server-filesystem",
                str(OUTPUT_DIR.resolve()),
            ],
            env={},
        ),
    })

    # 3. Custom Insights server
    insights_path = Path(__file__).parent.parent / "mcp_servers" / "insights_server.py"
    configs.append({
        "name": "insights",
        "params": StdioServerParameters(
            command=sys.executable,
            args=[str(insights_path)],
            env={},
        ),
    })

    return configs


# ── LLM helpers ───────────────────────────────────────────────────────────────

async def call_llm(messages: list[dict], tools_schema: list[dict]) -> dict:
    """
    Dispatch to the configured LLM backend.
    Retries up to RETRY_ATTEMPTS times on transient failures.
    """
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            if LLM_BACKEND == "groq":
                return await _call_groq(messages, tools_schema)
            elif LLM_BACKEND == "gemini":
                return await _call_gemini(messages, tools_schema)
            else:
                return await _call_ollama(messages, tools_schema)
        except Exception as exc:
            delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
            logger.warning(
                f"LLM call failed (attempt {attempt}/{RETRY_ATTEMPTS}): {exc}. "
                f"Retrying in {delay:.1f}s"
            )
            if attempt == RETRY_ATTEMPTS:
                raise
            await asyncio.sleep(delay)


async def _call_groq(messages: list[dict], tools: list[dict]) -> dict:
    """Groq — OpenAI-compatible endpoint."""
    payload = {
        "model": GROQ_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.2,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]


async def _call_gemini(messages: list[dict], tools: list[dict]) -> dict:
    """
    Google Gemini — via the OpenAI-compatible REST shim.
    Endpoint: https://generativelanguage.googleapis.com/v1beta/openai/chat/completions
    Requires GEMINI_API_KEY (from aistudio.google.com/apikey).
    """
    payload = {
        "model": GEMINI_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0.2,
    }
    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions",
            headers={
                "Authorization": f"Bearer {GEMINI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]


async def _call_ollama(messages: list[dict], tools: list[dict]) -> dict:
    """Ollama /api/chat — tool support requires Ollama ≥ 0.3."""
    payload = {
        "model": OLLAMA_MODEL,
        "messages": messages,
        "stream": False,
        "options": {"temperature": 0.2},
    }
    if tools:
        payload["tools"] = tools

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(f"{OLLAMA_BASE_URL}/api/chat", json=payload)
        resp.raise_for_status()
        msg = resp.json().get("message", {})
        return {
            "role": "assistant",
            "content": msg.get("content", ""),
            "tool_calls": msg.get("tool_calls", []),
        }


# ── Tool schema conversion ────────────────────────────────────────────────────

def mcp_tool_to_openai(server_name: str, tool) -> dict:
    """Convert an MCP tool definition to OpenAI function-calling format."""
    return {
        "type": "function",
        "function": {
            "name": f"{server_name}__{tool.name}",
            "description": f"[{server_name}] {tool.description}",
            "parameters": tool.inputSchema,
        },
    }


# ── Orchestrator ──────────────────────────────────────────────────────────────

class ResearchOrchestrator:
    """
    Manages connections to all MCP servers and drives the LLM planning loop.
    Yields event dicts for the UI to consume.
    """

    def __init__(self):
        self._sessions: dict[str, ClientSession] = {}

    async def run(self, user_goal: str) -> AsyncGenerator[dict, None]:
        """
        Main entry point. Yields event dicts:
          { type: "status" | "tool_call" | "tool_result" | "llm_thinking" | "final" | "error" }
        """
        configs = get_server_configs()
        yield {"type": "status", "message": f"Connecting to {len(configs)} MCP servers…"}

        queue: asyncio.Queue = asyncio.Queue()

        async def _inner():
            await self._open_all_and_run(configs, user_goal, queue)
            await queue.put(None)  # sentinel

        task = asyncio.create_task(_inner())
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
        await task

    async def _open_all_and_run(
        self,
        configs: list[dict],
        user_goal: str,
        queue: asyncio.Queue,
    ):
        """
        Open every MCP server sequentially (nested context managers),
        collect live sessions, then hand off to the planning loop.
        """
        sessions: dict[str, ClientSession] = {}

        for cfg in configs:
            name   = cfg["name"]
            params = cfg["params"]
            try:
                async with stdio_client(params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        sessions[name] = session
                        await queue.put({"type": "status", "message": f"✓ Connected: {name}"})
            except Exception as exc:
                await queue.put({
                    "type": "status",
                    "message": f"⚠ Could not connect to {name}: {exc}",
                })

        # Tool discovery
        tools_schema: list[dict] = []
        tool_map: dict[str, tuple[str, str]] = {}

        for server_name, session in sessions.items():
            try:
                result = await session.list_tools()
                for tool in result.tools:
                    full_name = f"{server_name}__{tool.name}"
                    tools_schema.append(mcp_tool_to_openai(server_name, tool))
                    tool_map[full_name] = (server_name, tool.name)
                    logger.debug(f"Tool discovered: {full_name}")
            except Exception as exc:
                await queue.put({
                    "type": "status",
                    "message": f"⚠ Tool discovery failed for {server_name}: {exc}",
                })

        await queue.put({
            "type": "status",
            "message": f"Discovered {len(tools_schema)} tools across {len(sessions)} servers",
        })

        await self._planning_loop(sessions, tools_schema, tool_map, user_goal, queue)

    async def _planning_loop(
        self,
        sessions:     dict,
        tools_schema: list[dict],
        tool_map:     dict,
        user_goal:    str,
        queue:        asyncio.Queue,
    ):
        """Core LLM ↔ tool iteration loop."""

        backend_label = LLM_BACKEND.upper()
        system_prompt = f"""You are a Smart Research Scout agent. Your job is to research a topic thoroughly using available tools.

You have access to MCP-based tools across three servers:
- **brave-search**: search the live web for current information
- **filesystem**: read and write files to persist research notes
- **insights**: summarize text, extract key points, format citations, merge notes

Recommended workflow:
1. Use brave-search (2–3 targeted queries) to gather raw information
2. Use insights__summarize_text on each result to condense it
3. Use insights__extract_key_points to pull bullet-point takeaways
4. Use insights__format_citations to format your sources
5. Use insights__merge_notes to compile everything into one document
6. Use filesystem__write_file to save the final note as a .md file
7. Reply with a concise summary for the user

Be thorough but efficient. Plan multiple steps ahead.
Today: {datetime.utcnow().strftime("%Y-%m-%d")}
Output directory: {OUTPUT_DIR.resolve()}
LLM backend: {backend_label}
"""

        messages: list[dict] = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_goal},
        ]

        notes_collected: list[str] = []
        step = 0

        while step < MAX_STEPS:
            step += 1
            await queue.put({
                "type": "status",
                "message": f"Step {step}/{MAX_STEPS}: asking {backend_label} to plan next action…",
            })

            # ── LLM call ──────────────────────────────────────────────────────
            try:
                response = await call_llm(messages, tools_schema)
            except Exception as exc:
                await queue.put({"type": "error", "message": f"LLM call failed: {exc}"})
                return

            messages.append(response)

            tool_calls = response.get("tool_calls") or []

            # No tool calls → LLM is done
            if not tool_calls:
                final_text = response.get("content") or "Research complete."
                await queue.put({"type": "final", "message": final_text})
                return

            # Emit reasoning text if present
            if response.get("content"):
                await queue.put({"type": "llm_thinking", "message": response["content"]})

            # ── Execute tool calls ────────────────────────────────────────────
            tool_results: list[dict] = []

            for tc in tool_calls:
                fn        = tc.get("function", {})
                full_name = fn.get("name", "")
                raw_args  = fn.get("arguments", "{}")
                call_id   = tc.get("id", f"call_{step}")

                try:
                    arguments = json.loads(raw_args) if isinstance(raw_args, str) else raw_args
                except json.JSONDecodeError:
                    arguments = {}

                await queue.put({
                    "type":      "tool_call",
                    "tool":      full_name,
                    "arguments": _safe_log(arguments),
                    "call_id":   call_id,
                })

                # Execute with retries
                output = await self._execute_tool(full_name, arguments, tool_map, sessions)

                # Track notes for fallback summary
                if "summarize" in full_name or "merge" in full_name:
                    notes_collected.append(output[:200] + "…" if len(output) > 200 else output)

                logger.info(f"Tool result for {full_name}: {len(output)} chars")

                await queue.put({
                    "type":           "tool_result",
                    "tool":           full_name,
                    "output_preview": output[:400] + ("…" if len(output) > 400 else ""),
                    "output_full":    output,
                    "call_id":        call_id,
                })

                tool_results.append({
                    "tool_call_id": call_id,
                    "role":         "tool",
                    "content":      output,
                })

            messages.extend(tool_results)

        # Max steps exceeded
        await queue.put({
            "type":    "final",
            "message": (
                f"Reached maximum steps ({MAX_STEPS}). Research collected:\n"
                + "\n".join(notes_collected[:3])
            ),
        })

    async def _execute_tool(
        self,
        full_name: str,
        arguments: dict,
        tool_map:  dict,
        sessions:  dict,
    ) -> str:
        """Execute a single tool call with retries; always returns a string."""
        if full_name not in tool_map:
            return f"ERROR: Unknown tool '{full_name}'"

        server_name, tool_name = tool_map[full_name]
        session = sessions.get(server_name)
        if not session:
            return f"ERROR: Server '{server_name}' is not connected"

        for attempt in range(1, RETRY_ATTEMPTS + 1):
            try:
                logger.info(
                    f"Calling {full_name} (attempt {attempt}) | args: {_safe_log(arguments)}"
                )
                result = await session.call_tool(tool_name, arguments)
                return "\n".join(
                    block.text if hasattr(block, "text") else str(block)
                    for block in result.content
                )
            except Exception as exc:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                logger.warning(f"Tool {full_name} attempt {attempt} failed: {exc}")
                if attempt == RETRY_ATTEMPTS:
                    return f"ERROR after {RETRY_ATTEMPTS} attempts: {exc}"
                await asyncio.sleep(delay)

        return "ERROR: unexpected exit from retry loop"


# ── Utility ───────────────────────────────────────────────────────────────────

def _safe_log(d: dict) -> str:
    """Return a JSON string with secret-looking keys redacted."""
    safe = {}
    for k, v in d.items():
        if any(word in k.lower() for word in ("key", "secret", "token", "password")):
            safe[k] = "***"
        elif isinstance(v, str) and len(v) > 200:
            safe[k] = v[:200] + "…"
        else:
            safe[k] = v
    return json.dumps(safe)


# ── CLI entry point ───────────────────────────────────────────────────────────

async def _cli_main():
    goal = " ".join(sys.argv[1:]) or "Research the latest developments in quantum computing."
    orch = ResearchOrchestrator()
    print(f"\n🎯 Goal: {goal}\n{'─' * 60}")

    async for event in orch.run(goal):
        t = event.get("type")
        if t == "status":
            print(f"  ⏳ {event['message']}")
        elif t == "llm_thinking":
            print(f"\n💭 LLM: {event['message'][:300]}")
        elif t == "tool_call":
            print(f"\n🔧 CALL {event['tool']}: {event['arguments'][:150]}")
        elif t == "tool_result":
            print(f"   └─ Result: {event['output_preview'][:200]}")
        elif t == "final":
            print(f"\n✅ DONE:\n{event['message']}")
        elif t == "error":
            print(f"\n❌ ERROR: {event['message']}")


if __name__ == "__main__":
    asyncio.run(_cli_main())
