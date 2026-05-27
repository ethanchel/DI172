"""
Smart Research Scout — Streamlit UI
─────────────────────────────────────────────────────────────────────────────
A polished, terminal-noir research interface that drives the MCP orchestrator.
"""

import asyncio
import json
import os
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Add project root to path
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from client.orchestrator import ResearchOrchestrator, OUTPUT_DIR, LLM_BACKEND

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Smart Research Scout",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@300;400;600&family=IBM+Plex+Sans:wght@300;400;700&display=swap');

:root {
  --bg: #0a0a0f;
  --surface: #111118;
  --border: #1e1e2e;
  --accent: #00d4aa;
  --accent2: #7c3aed;
  --warn: #f59e0b;
  --error: #ef4444;
  --text: #e2e8f0;
  --muted: #64748b;
  --mono: 'IBM Plex Mono', monospace;
  --sans: 'IBM Plex Sans', sans-serif;
}

html, body, [class*="css"] {
  font-family: var(--sans) !important;
  background-color: var(--bg) !important;
  color: var(--text) !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: var(--surface) !important;
  border-right: 1px solid var(--border);
}

/* Main content */
.main .block-container {
  padding: 2rem 2rem;
  max-width: 1100px;
}

/* Hero */
.hero-title {
  font-family: var(--mono);
  font-size: clamp(1.6rem, 3vw, 2.4rem);
  font-weight: 600;
  color: var(--accent);
  letter-spacing: -0.02em;
  line-height: 1.1;
  margin: 0;
}
.hero-sub {
  font-family: var(--mono);
  font-size: 0.78rem;
  color: var(--muted);
  margin-top: 0.3rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

/* Goal input */
.stTextArea textarea {
  font-family: var(--mono) !important;
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
  font-size: 0.95rem !important;
}
.stTextArea textarea:focus {
  border-color: var(--accent) !important;
  box-shadow: 0 0 0 2px rgba(0,212,170,0.12) !important;
}

/* Run button */
.stButton > button {
  background: var(--accent) !important;
  color: #0a0a0f !important;
  font-family: var(--mono) !important;
  font-weight: 600 !important;
  font-size: 0.9rem !important;
  border: none !important;
  border-radius: 6px !important;
  padding: 0.6rem 1.6rem !important;
  letter-spacing: 0.06em !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover {
  background: #00f0c0 !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 16px rgba(0,212,170,0.3) !important;
}

/* Event cards */
.event-card {
  border-radius: 8px;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-family: var(--mono);
  font-size: 0.82rem;
  line-height: 1.6;
  border-left: 3px solid transparent;
  background: var(--surface);
}
.event-status {
  border-left-color: var(--muted);
  color: var(--muted);
}
.event-tool-call {
  border-left-color: var(--accent2);
  color: #a78bfa;
  background: rgba(124, 58, 237, 0.06);
}
.event-tool-result {
  border-left-color: var(--accent);
  background: rgba(0, 212, 170, 0.04);
  color: var(--text);
}
.event-thinking {
  border-left-color: var(--warn);
  background: rgba(245, 158, 11, 0.05);
  color: #fbbf24;
  font-style: italic;
}
.event-final {
  border-left-color: var(--accent);
  background: rgba(0,212,170,0.07);
  color: var(--text);
  font-family: var(--sans);
  font-size: 0.9rem;
}
.event-error {
  border-left-color: var(--error);
  background: rgba(239,68,68,0.07);
  color: #fca5a5;
}

/* Tool badge */
.tool-badge {
  display: inline-block;
  background: rgba(124,58,237,0.2);
  color: #a78bfa;
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.7rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  margin-right: 0.4rem;
}
.tool-badge-search { background: rgba(59,130,246,0.2); color: #93c5fd; }
.tool-badge-fs { background: rgba(16,185,129,0.2); color: #6ee7b7; }
.tool-badge-insights { background: rgba(245,158,11,0.2); color: #fcd34d; }

/* Metrics */
.metric-row {
  display: flex;
  gap: 1rem;
  margin: 1rem 0;
}
.metric-box {
  flex: 1;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  text-align: center;
}
.metric-val {
  font-family: var(--mono);
  font-size: 1.8rem;
  font-weight: 600;
  color: var(--accent);
}
.metric-label {
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
}

/* Config pills */
.config-pill {
  display: inline-block;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.25rem 0.6rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  color: var(--muted);
  margin: 0.15rem;
}
.config-pill.active { border-color: var(--accent); color: var(--accent); }

/* Sidebar sections */
.sidebar-section {
  font-family: var(--mono);
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin: 1.2rem 0 0.4rem;
}

/* Log viewer */
.log-viewer {
  background: #070710;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  font-family: var(--mono);
  font-size: 0.72rem;
  color: #64748b;
  max-height: 300px;
  overflow-y: auto;
  line-height: 1.7;
}

/* Divider */
hr {
  border: none;
  border-top: 1px solid var(--border) !important;
  margin: 1.5rem 0 !important;
}

/* Expander */
.streamlit-expanderHeader {
  font-family: var(--mono) !important;
  font-size: 0.8rem !important;
  color: var(--muted) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* Spinner color override */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* Select / Input overrides */
.stSelectbox select, .stTextInput input {
  background: var(--surface) !important;
  color: var(--text) !important;
  border-color: var(--border) !important;
  font-family: var(--mono) !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────

def init_state():
    defaults = {
        "events": [],
        "running": False,
        "finished": False,
        "stats": {"steps": 0, "tools_called": 0, "notes_saved": 0, "elapsed": 0},
        "log_lines": [],
        "final_note_path": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem;">
      <div style="font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; font-weight: 600; color: #00d4aa;">
        RESEARCH SCOUT
      </div>
      <div style="font-size: 0.65rem; color: #475569; letter-spacing: 0.15em; text-transform: uppercase; margin-top: 2px;">
        MCP · LLM · AGENTIC
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="sidebar-section">LLM Backend</div>', unsafe_allow_html=True)
    llm_backend = st.selectbox(
        "Backend",
        ["groq", "ollama"],
        index=0 if LLM_BACKEND == "groq" else 1,
        label_visibility="collapsed",
    )
    os.environ["LLM_BACKEND"] = llm_backend

    if llm_backend == "groq":
        groq_key = st.text_input(
            "Groq API Key",
            value=os.getenv("GROQ_API_KEY", ""),
            type="password",
            placeholder="gsk_…",
        )
        if groq_key:
            os.environ["GROQ_API_KEY"] = groq_key

        groq_model = st.selectbox(
            "Model",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"],
            index=0,
        )
        os.environ["GROQ_MODEL"] = groq_model
    else:
        ollama_url = st.text_input("Ollama URL", value="http://localhost:11434")
        os.environ["OLLAMA_BASE_URL"] = ollama_url
        ollama_model = st.text_input("Model", value="llama3")
        os.environ["OLLAMA_MODEL"] = ollama_model

    st.markdown("---")
    st.markdown('<div class="sidebar-section">MCP Servers</div>', unsafe_allow_html=True)

    brave_key = st.text_input(
        "Brave Search API Key",
        value=os.getenv("BRAVE_API_KEY", ""),
        type="password",
        placeholder="BSA…",
        help="Get a free key at search.brave.com/app/keys",
    )
    if brave_key:
        os.environ["BRAVE_API_KEY"] = brave_key

    st.markdown('<div class="sidebar-section">Servers</div>', unsafe_allow_html=True)

    server_status = {
        "brave-search": "🟢" if brave_key else "🔴",
        "filesystem": "🟢",
        "insights (custom)": "🟢",
    }
    for srv, status in server_status.items():
        st.markdown(
            f'<span class="config-pill {"active" if status == "🟢" else ""}">'
            f'{status} {srv}</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown('<div class="sidebar-section">Output</div>', unsafe_allow_html=True)
    st.markdown(
        f'<span class="config-pill">{OUTPUT_DIR.resolve()}</span>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    # Quick examples
    st.markdown('<div class="sidebar-section">Example Goals</div>', unsafe_allow_html=True)
    examples = [
        "Research the latest breakthroughs in fusion energy in 2024-2025",
        "Summarize current trends in large language model efficiency",
        "What are the top open-source alternatives to GPT-4 right now?",
    ]
    for ex in examples:
        if st.button(ex[:48] + "…" if len(ex) > 48 else ex, key=ex, use_container_width=True):
            st.session_state["goal_preset"] = ex


# ── Main UI ───────────────────────────────────────────────────────────────────

col_title, col_meta = st.columns([3, 1])
with col_title:
    st.markdown("""
    <div class="hero-title">🔍 Smart Research Scout</div>
    <div class="hero-sub">Web Search · File System · Insights · MCP Orchestration</div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Goal input
preset = st.session_state.pop("goal_preset", "")
goal = st.text_area(
    "Research Goal",
    value=preset or "Research the latest breakthroughs in quantum error correction in 2025.",
    height=100,
    placeholder="Enter your research goal…",
    label_visibility="collapsed",
)

col_run, col_clear, col_spacer = st.columns([1, 1, 4])
with col_run:
    run_btn = st.button("▶ Run Scout", disabled=st.session_state["running"], use_container_width=True)
with col_clear:
    if st.button("⟳ Clear", use_container_width=True):
        st.session_state["events"] = []
        st.session_state["finished"] = False
        st.session_state["running"] = False
        st.session_state["stats"] = {"steps": 0, "tools_called": 0, "notes_saved": 0, "elapsed": 0}
        st.session_state["log_lines"] = []
        st.session_state["final_note_path"] = None
        st.rerun()

# ── Metrics row ───────────────────────────────────────────────────────────────

if st.session_state["stats"]["steps"] > 0 or st.session_state["running"]:
    s = st.session_state["stats"]
    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-box">
        <div class="metric-val">{s['steps']}</div>
        <div class="metric-label">Steps</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{s['tools_called']}</div>
        <div class="metric-label">Tool Calls</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{s['notes_saved']}</div>
        <div class="metric-label">Files Saved</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{s['elapsed']:.1f}s</div>
        <div class="metric-label">Elapsed</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Event stream ──────────────────────────────────────────────────────────────

def tool_badge(tool_name: str) -> str:
    if "brave" in tool_name or "search" in tool_name:
        cls = "tool-badge-search"
    elif "filesystem" in tool_name:
        cls = "tool-badge-fs"
    else:
        cls = "tool-badge-insights"
    short = tool_name.split("__")[-1] if "__" in tool_name else tool_name
    return f'<span class="tool-badge {cls}">{short}</span>'


def render_event(ev: dict) -> str:
    t = ev.get("type")
    if t == "status":
        return f'<div class="event-card event-status">⟳ {ev["message"]}</div>'
    elif t == "llm_thinking":
        msg = ev["message"][:400].replace("<", "&lt;")
        return f'<div class="event-card event-thinking">💭 {msg}</div>'
    elif t == "tool_call":
        badge = tool_badge(ev["tool"])
        args = ev.get("arguments", "")[:200].replace("<", "&lt;")
        return f'<div class="event-card event-tool-call">{badge} <strong>{ev["tool"]}</strong><br><span style="opacity:0.7;font-size:0.75rem">{args}</span></div>'
    elif t == "tool_result":
        badge = tool_badge(ev["tool"])
        preview = ev.get("output_preview", "")[:300].replace("<", "&lt;").replace("\n", "<br>")
        return f'<div class="event-card event-tool-result">{badge} → {preview}</div>'
    elif t == "final":
        msg = ev["message"].replace("<", "&lt;").replace("\n", "<br>")
        return f'<div class="event-card event-final">✅ <strong>DONE</strong><br><br>{msg}</div>'
    elif t == "error":
        return f'<div class="event-card event-error">❌ {ev["message"]}</div>'
    return ""


event_container = st.empty()


def refresh_events():
    cards = "".join(render_event(e) for e in st.session_state["events"])
    event_container.markdown(
        f'<div style="max-height:520px;overflow-y:auto;padding-right:4px">{cards}</div>',
        unsafe_allow_html=True,
    )


refresh_events()

# ── Final note viewer ─────────────────────────────────────────────────────────

if st.session_state.get("final_note_path"):
    fp = Path(st.session_state["final_note_path"])
    if fp.exists():
        with st.expander("📄 View saved research note", expanded=True):
            st.markdown(fp.read_text())
        with open(fp, "rb") as f:
            st.download_button(
                "⬇ Download note",
                data=f,
                file_name=fp.name,
                mime="text/markdown",
            )

# ── Run logic ─────────────────────────────────────────────────────────────────

async def run_orchestrator(goal: str):
    """Run the orchestrator and push events into session state."""
    orch = ResearchOrchestrator()
    start = time.time()

    async for event in orch.run(goal):
        st.session_state["events"].append(event)

        t = event.get("type")
        if t == "tool_call":
            st.session_state["stats"]["tools_called"] += 1
        if t in ("tool_call", "tool_result", "llm_thinking"):
            st.session_state["stats"]["steps"] += 1
        if t == "tool_result" and "write" in event.get("tool", ""):
            st.session_state["stats"]["notes_saved"] += 1
            # Try to extract saved path from output
            out = event.get("output_full", "")
            for line in out.split("\n"):
                if OUTPUT_DIR.name in line or str(OUTPUT_DIR) in line:
                    candidate = line.strip()
                    if candidate.endswith(".md"):
                        st.session_state["final_note_path"] = candidate

        st.session_state["stats"]["elapsed"] = time.time() - start


if run_btn and goal.strip():
    st.session_state["running"] = True
    st.session_state["events"] = []
    st.session_state["finished"] = False
    st.session_state["stats"] = {"steps": 0, "tools_called": 0, "notes_saved": 0, "elapsed": 0}

    # Run in a background thread so Streamlit stays responsive
    result_ready = threading.Event()
    error_holder = [None]

    def _thread_target():
        try:
            asyncio.run(run_orchestrator(goal))
        except Exception as exc:
            error_holder[0] = exc
        finally:
            result_ready.set()

    thread = threading.Thread(target=_thread_target, daemon=True)
    thread.start()

    # Poll while running
    with st.spinner("Scout is researching…"):
        while not result_ready.is_set():
            time.sleep(0.8)
            refresh_events()
            st.rerun()

    thread.join(timeout=5)

    if error_holder[0]:
        st.session_state["events"].append({
            "type": "error",
            "message": str(error_holder[0]),
        })

    st.session_state["running"] = False
    st.session_state["finished"] = True
    refresh_events()
    st.rerun()


# ── Log viewer ────────────────────────────────────────────────────────────────

log_file = Path(os.getenv("LOG_FILE", "./logs/scout.log"))
if log_file.exists():
    with st.expander("🖥 Live log", expanded=False):
        lines = log_file.read_text().split("\n")[-60:]
        log_html = "\n".join(lines)
        st.markdown(
            f'<div class="log-viewer">{log_html}</div>',
            unsafe_allow_html=True,
        )

# ── Architecture diagram ──────────────────────────────────────────────────────

with st.expander("🗺 Architecture", expanded=False):
    st.markdown("""
```
┌──────────────────────────────────────────────────────────────────────┐
│                     Smart Research Scout                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   User Goal (Streamlit)                                              │
│        │                                                             │
│        ▼                                                             │
│   ResearchOrchestrator (client/orchestrator.py)                      │
│        │                                                             │
│        │   System prompt + available tools → LLM                    │
│        │   LLM returns tool_calls (JSON)                             │
│        │   Execute → append result → re-prompt                       │
│        │                                                             │
│   ┌────┴──────────────┬────────────────────────────┐                │
│   ▼                   ▼                            ▼                │
│ brave-search MCP   filesystem MCP          insights MCP (custom)    │
│ (3rd party)        (3rd party)             (mcp_servers/)           │
│   web_search       read_file               summarize_text           │
│                    write_file              extract_key_points        │
│                    list_directory          format_citations          │
│                                            merge_notes              │
│                                                                      │
│   Config: .env (GROQ_API_KEY / OLLAMA, BRAVE_API_KEY)               │
│   Logs:   ./logs/scout.log                                           │
│   Output: ./outputs/*.md                                             │
└──────────────────────────────────────────────────────────────────────┘
```
    """)

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown("""
<div style="text-align:center;padding:2rem 0 0.5rem;font-family:'IBM Plex Mono',monospace;
font-size:0.65rem;color:#334155;letter-spacing:0.1em;">
SMART RESEARCH SCOUT · MCP + LLM AGENTIC PIPELINE · ≥2 THIRD-PARTY SERVERS
</div>
""", unsafe_allow_html=True)
