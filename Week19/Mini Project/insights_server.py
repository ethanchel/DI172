"""
Custom Insights MCP Server
─────────────────────────────────────────────────────────────────────────────
Provides tools for:
  • summarize_text  — condense raw text into a structured research note
  • format_citations — clean and format a list of URL sources
  • extract_key_points — pull bullet-point takeaways from text
  • merge_notes — combine multiple research notes into one document

Run standalone:  python mcp_servers/insights_server.py
"""

import json
import re
import textwrap
from datetime import datetime
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types

server = Server("insights-server")


# ── Tool: summarize_text ──────────────────────────────────────────────────────
@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="summarize_text",
            description=(
                "Condense raw text into a structured research note with a title, "
                "summary paragraph, and key takeaways. Returns markdown."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Raw text to summarize"},
                    "topic": {"type": "string", "description": "Topic/title for the note"},
                    "max_words": {
                        "type": "integer",
                        "description": "Approximate max words for summary (default 120)",
                        "default": 120,
                    },
                },
                "required": ["text", "topic"],
            },
        ),
        types.Tool(
            name="format_citations",
            description=(
                "Take a list of URLs and optional titles, and return a clean "
                "numbered citation list in APA-style markdown."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url": {"type": "string"},
                                "title": {"type": "string"},
                            },
                            "required": ["url"],
                        },
                        "description": "List of source objects with url and optional title",
                    }
                },
                "required": ["sources"],
            },
        ),
        types.Tool(
            name="extract_key_points",
            description=(
                "Extract up to N concise bullet-point key points from a body of text."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "Text to extract from"},
                    "max_points": {
                        "type": "integer",
                        "description": "Maximum bullet points to return (default 6)",
                        "default": 6,
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="merge_notes",
            description=(
                "Merge multiple markdown research note strings into one cohesive document "
                "with a table of contents."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notes": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of markdown note strings to merge",
                    },
                    "document_title": {
                        "type": "string",
                        "description": "Title for the merged document",
                    },
                },
                "required": ["notes", "document_title"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "summarize_text":
        return _summarize_text(arguments)
    elif name == "format_citations":
        return _format_citations(arguments)
    elif name == "extract_key_points":
        return _extract_key_points(arguments)
    elif name == "merge_notes":
        return _merge_notes(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


# ── Implementations ───────────────────────────────────────────────────────────

def _summarize_text(args: dict) -> list[types.TextContent]:
    text = args["text"].strip()
    topic = args["topic"].strip()
    max_words = int(args.get("max_words", 120))

    # Naive summarization: take first sentences up to word limit
    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary_sentences = []
    word_count = 0
    for s in sentences:
        words = len(s.split())
        if word_count + words > max_words:
            break
        summary_sentences.append(s)
        word_count += words

    summary = " ".join(summary_sentences) if summary_sentences else text[:500]

    # Key points: first 3 distinct sentences not used in summary
    remaining = [s for s in sentences if s not in summary_sentences][:3]
    bullets = "\n".join(f"- {s.strip()}" for s in remaining if s.strip())

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    note = textwrap.dedent(f"""\
        # {topic}

        > *Research note generated {timestamp}*

        ## Summary

        {summary}

        ## Key Points

        {bullets if bullets else "- See summary above."}
    """)

    return [types.TextContent(type="text", text=note)]


def _format_citations(args: dict) -> list[types.TextContent]:
    sources = args["sources"]
    lines = []
    for i, src in enumerate(sources, 1):
        url = src.get("url", "")
        title = src.get("title") or _infer_title_from_url(url)
        # Simple APA-style: Author/Site (n.d.). Title. URL
        domain = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
        lines.append(f"{i}. {domain} (n.d.). *{title}*. Retrieved from {url}")

    result = "## References\n\n" + "\n\n".join(lines)
    return [types.TextContent(type="text", text=result)]


def _extract_key_points(args: dict) -> list[types.TextContent]:
    text = args["text"].strip()
    max_points = int(args.get("max_points", 6))

    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Filter: prefer longer, more informative sentences
    scored = sorted(sentences, key=lambda s: len(s), reverse=True)
    selected = [s.strip() for s in scored[:max_points] if len(s.strip()) > 20]

    bullets = "\n".join(f"- {s}" for s in selected)
    result = f"## Key Points\n\n{bullets}" if bullets else "## Key Points\n\n- No key points extracted."
    return [types.TextContent(type="text", text=result)]


def _merge_notes(args: dict) -> list[types.TextContent]:
    notes = args["notes"]
    title = args["document_title"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Build table of contents
    toc_lines = []
    sections = []
    for i, note in enumerate(notes, 1):
        # Extract first H1 as section title
        match = re.search(r'^#\s+(.+)$', note, re.MULTILINE)
        section_title = match.group(1) if match else f"Section {i}"
        anchor = re.sub(r'[^a-z0-9-]', '', section_title.lower().replace(' ', '-'))
        toc_lines.append(f"{i}. [{section_title}](#{anchor})")
        sections.append(note.strip())

    toc = "\n".join(toc_lines)
    body = "\n\n---\n\n".join(sections)

    merged = textwrap.dedent(f"""\
        # {title}

        > *Compiled {timestamp}*

        ## Table of Contents

        {toc}

        ---

        {body}
    """)
    return [types.TextContent(type="text", text=merged)]


def _infer_title_from_url(url: str) -> str:
    path = url.rstrip('/').split('/')[-1]
    title = re.sub(r'[-_]', ' ', path).replace('.html', '').replace('.htm', '')
    return title.title() if title else url


# ── Entry point ───────────────────────────────────────────────────────────────

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
