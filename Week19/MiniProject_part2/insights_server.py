"""
Custom Insights MCP Server  (Part 2 — extended)
─────────────────────────────────────────────────────────────────────────────
Tools:
  Part 1 (unchanged)
  • summarize_text        — condense raw text into a structured research note
  • format_citations      — APA-style citation list from URLs
  • extract_key_points    — bullet-point takeaways from text
  • merge_notes           — combine multiple notes into one document

  Part 2 (new — non-trivial custom tools)
  • analyze_sentiment     — lexicon-based sentiment scoring + emotional keywords
  • assess_source_credibility — heuristic credibility score for a web source

Run standalone:  python mcp_servers/insights_server.py
"""

import math
import re
import textwrap
from collections import Counter
from datetime import datetime

from mcp import types
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("insights-server")


# ═══════════════════════════════════════════════════════════════════════════════
# Sentiment lexicon (no external dependencies)
# Positive / negative word lists + intensifiers + negations
# ═══════════════════════════════════════════════════════════════════════════════

_POSITIVE_WORDS = {
    "breakthrough", "innovative", "excellent", "outstanding", "remarkable",
    "significant", "successful", "promising", "impressive", "revolutionary",
    "advance", "improve", "benefit", "achieve", "gain", "efficient",
    "effective", "powerful", "accurate", "robust", "reliable", "fast",
    "accurate", "strong", "positive", "growth", "progress", "discovery",
    "solution", "optimized", "scalable", "stable", "secure", "safe",
    "enhance", "boost", "enable", "support", "lead", "exceed", "surpass",
    "record", "unprecedented", "groundbreaking", "milestone", "win",
    "superior", "dominant", "flourish", "thrive", "accelerate",
}

_NEGATIVE_WORDS = {
    "failure", "problem", "issue", "concern", "risk", "danger", "threat",
    "difficult", "challenge", "limitation", "flaw", "weakness", "error",
    "vulnerability", "attack", "breach", "loss", "decline", "fall",
    "drop", "decrease", "worsen", "costly", "expensive", "slow", "poor",
    "inadequate", "inefficient", "unreliable", "unstable", "harmful",
    "toxic", "dangerous", "critical", "severe", "serious", "alarming",
    "controversial", "dispute", "conflict", "obstacle", "barrier",
    "setback", "crisis", "collapse", "fail", "broken", "flawed",
}

_INTENSIFIERS = {"very", "extremely", "highly", "significantly", "greatly", "deeply"}
_NEGATIONS    = {"not", "no", "never", "neither", "nor", "without", "lack", "hardly"}

# Credibility signals
_CREDIBLE_TLDS    = {".edu", ".gov", ".org", ".ac.uk", ".ac.fr"}
_CREDIBLE_DOMAINS = {
    "nature.com", "science.org", "pubmed.ncbi.nlm.nih.gov", "arxiv.org",
    "ieee.org", "acm.org", "bbc.com", "reuters.com", "apnews.com",
    "theguardian.com", "nytimes.com", "washingtonpost.com", "economist.com",
    "mit.edu", "stanford.edu", "harvard.edu", "cambridge.org", "springer.com",
    "sciencedirect.com", "jstor.org", "ncbi.nlm.nih.gov", "who.int",
}
_LOW_CRED_SIGNALS = {
    "click", "viral", "shocking", "secret", "trick", "hack", "unbelievable",
    "you won't believe", "they don't want you", "exposed", "conspiracy",
}


# ═══════════════════════════════════════════════════════════════════════════════
# Tool registry
# ═══════════════════════════════════════════════════════════════════════════════

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        # ── Part 1 tools ──────────────────────────────────────────────────────
        types.Tool(
            name="summarize_text",
            description=(
                "Condense raw text into a structured research note with a title, "
                "summary paragraph, and key takeaways. Returns markdown."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text":      {"type": "string",  "description": "Raw text to summarize"},
                    "topic":     {"type": "string",  "description": "Topic/title for the note"},
                    "max_words": {"type": "integer", "description": "Approx max words (default 120)", "default": 120},
                },
                "required": ["text", "topic"],
            },
        ),
        types.Tool(
            name="format_citations",
            description=(
                "Take a list of URLs and optional titles and return a clean "
                "numbered APA-style citation list in markdown."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "sources": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "url":   {"type": "string"},
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
            description="Extract up to N concise bullet-point key points from a body of text.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text":       {"type": "string",  "description": "Text to extract from"},
                    "max_points": {"type": "integer", "description": "Max bullet points (default 6)", "default": 6},
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="merge_notes",
            description=(
                "Merge multiple markdown research note strings into one cohesive "
                "document with a table of contents."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "notes":          {"type": "array", "items": {"type": "string"}, "description": "Markdown note strings"},
                    "document_title": {"type": "string", "description": "Title for the merged document"},
                },
                "required": ["notes", "document_title"],
            },
        ),

        # ── Part 2 tools (new) ────────────────────────────────────────────────
        types.Tool(
            name="analyze_sentiment",
            description=(
                "Perform lexicon-based sentiment analysis on a text. "
                "Returns a sentiment label (Positive / Neutral / Negative), "
                "a polarity score from -1.0 (most negative) to +1.0 (most positive), "
                "a confidence percentage, and the top emotional keywords found. "
                "Useful for gauging the tone of search results or research articles."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to analyse (article snippet, search result, note, etc.)",
                    },
                    "context_label": {
                        "type": "string",
                        "description": "Optional label for the source (e.g. article title) included in output",
                        "default": "",
                    },
                },
                "required": ["text"],
            },
        ),
        types.Tool(
            name="assess_source_credibility",
            description=(
                "Heuristically assess the credibility of a web source given its URL and "
                "an optional text snippet from the page. "
                "Returns a credibility score (0–100), a tier label "
                "(High / Medium / Low), and a list of signals that influenced the score. "
                "Useful for filtering low-quality sources before summarising."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "Full URL of the source to evaluate",
                    },
                    "snippet": {
                        "type": "string",
                        "description": "Optional text snippet from the page (improves accuracy)",
                        "default": "",
                    },
                    "title": {
                        "type": "string",
                        "description": "Optional page title",
                        "default": "",
                    },
                },
                "required": ["url"],
            },
        ),
    ]


# ═══════════════════════════════════════════════════════════════════════════════
# Dispatcher
# ═══════════════════════════════════════════════════════════════════════════════

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    handlers = {
        "summarize_text":          _summarize_text,
        "format_citations":        _format_citations,
        "extract_key_points":      _extract_key_points,
        "merge_notes":             _merge_notes,
        "analyze_sentiment":       _analyze_sentiment,
        "assess_source_credibility": _assess_source_credibility,
    }
    if name not in handlers:
        raise ValueError(f"Unknown tool: {name}")
    return handlers[name](arguments)


# ═══════════════════════════════════════════════════════════════════════════════
# Part 1 implementations (unchanged)
# ═══════════════════════════════════════════════════════════════════════════════

def _summarize_text(args: dict) -> list[types.TextContent]:
    text      = args["text"].strip()
    topic     = args["topic"].strip()
    max_words = int(args.get("max_words", 120))

    sentences = re.split(r'(?<=[.!?])\s+', text)
    summary_sentences, word_count = [], 0
    for s in sentences:
        w = len(s.split())
        if word_count + w > max_words:
            break
        summary_sentences.append(s)
        word_count += w

    summary  = " ".join(summary_sentences) if summary_sentences else text[:500]
    remaining = [s for s in sentences if s not in summary_sentences][:3]
    bullets   = "\n".join(f"- {s.strip()}" for s in remaining if s.strip())
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
    lines   = []
    for i, src in enumerate(sources, 1):
        url    = src.get("url", "")
        title  = src.get("title") or _infer_title_from_url(url)
        domain = re.sub(r'^https?://(www\.)?', '', url).split('/')[0]
        lines.append(f"{i}. {domain} (n.d.). *{title}*. Retrieved from {url}")
    result = "## References\n\n" + "\n\n".join(lines)
    return [types.TextContent(type="text", text=result)]


def _extract_key_points(args: dict) -> list[types.TextContent]:
    text       = args["text"].strip()
    max_points = int(args.get("max_points", 6))
    sentences  = re.split(r'(?<=[.!?])\s+', text)
    scored     = sorted(sentences, key=lambda s: len(s), reverse=True)
    selected   = [s.strip() for s in scored[:max_points] if len(s.strip()) > 20]
    bullets    = "\n".join(f"- {s}" for s in selected)
    result     = f"## Key Points\n\n{bullets}" if bullets else "## Key Points\n\n- No key points extracted."
    return [types.TextContent(type="text", text=result)]


def _merge_notes(args: dict) -> list[types.TextContent]:
    notes     = args["notes"]
    title     = args["document_title"]
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    toc_lines, sections = [], []
    for i, note in enumerate(notes, 1):
        match         = re.search(r'^#\s+(.+)$', note, re.MULTILINE)
        section_title = match.group(1) if match else f"Section {i}"
        anchor        = re.sub(r'[^a-z0-9-]', '', section_title.lower().replace(' ', '-'))
        toc_lines.append(f"{i}. [{section_title}](#{anchor})")
        sections.append(note.strip())
    toc  = "\n".join(toc_lines)
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
    path  = url.rstrip('/').split('/')[-1]
    title = re.sub(r'[-_]', ' ', path).replace('.html', '').replace('.htm', '')
    return title.title() if title else url


# ═══════════════════════════════════════════════════════════════════════════════
# Part 2 — Tool 1: analyze_sentiment
# ═══════════════════════════════════════════════════════════════════════════════

def _analyze_sentiment(args: dict) -> list[types.TextContent]:
    """
    Lexicon-based sentiment analysis.

    Algorithm:
      1. Tokenise text into lowercase words.
      2. Slide a window of 3: if a negation precedes a word, flip its polarity.
         If an intensifier precedes a word, multiply its weight by 1.5.
      3. Aggregate weighted positive / negative counts.
      4. Polarity = (pos - neg) / (pos + neg + ε)  → [-1, +1]
      5. Confidence = tanh(|raw_score| / 5) * 100  → [0, 100]%
      6. Extract top emotional keywords (positive + negative hits).
    """
    text          = args.get("text", "").strip()
    context_label = args.get("context_label", "")

    if not text:
        return [types.TextContent(type="text", text="ERROR: empty text provided")]

    tokens = re.findall(r"[a-z']+", text.lower())
    n      = len(tokens)

    pos_score = 0.0
    neg_score = 0.0
    pos_hits: list[str] = []
    neg_hits: list[str] = []

    for i, token in enumerate(tokens):
        # Look-back window for negation / intensification
        window     = tokens[max(0, i - 3): i]
        negated    = any(w in _NEGATIONS    for w in window)
        intensified = any(w in _INTENSIFIERS for w in window)
        weight     = 1.5 if intensified else 1.0

        if token in _POSITIVE_WORDS:
            if negated:
                neg_score += weight
                neg_hits.append(f"not {token}")
            else:
                pos_score += weight
                pos_hits.append(token)

        elif token in _NEGATIVE_WORDS:
            if negated:
                pos_score += weight * 0.5   # double-negative is mildly positive
                pos_hits.append(f"not {token}")
            else:
                neg_score += weight
                neg_hits.append(token)

    total    = pos_score + neg_score
    polarity = (pos_score - neg_score) / (total + 1e-9)  # [-1, +1]
    raw_diff = pos_score - neg_score
    confidence = round(math.tanh(abs(raw_diff) / max(5, n / 20)) * 100, 1)

    # Label
    if polarity > 0.15:
        label, emoji = "Positive", "🟢"
    elif polarity < -0.15:
        label, emoji = "Negative", "🔴"
    else:
        label, emoji = "Neutral", "🟡"

    # Top keywords (deduplicated, by frequency)
    top_pos = [w for w, _ in Counter(pos_hits).most_common(5)]
    top_neg = [w for w, _ in Counter(neg_hits).most_common(5)]

    # Sentence-level breakdown (first 5 sentences)
    sentences = re.split(r'(?<=[.!?])\s+', text)[:5]
    sent_lines = []
    for s in sentences:
        s_tokens = re.findall(r"[a-z']+", s.lower())
        s_pos = sum(1 for t in s_tokens if t in _POSITIVE_WORDS)
        s_neg = sum(1 for t in s_tokens if t in _NEGATIVE_WORDS)
        if s_pos > s_neg:
            tone = "⊕"
        elif s_neg > s_pos:
            tone = "⊖"
        else:
            tone = "○"
        sent_lines.append(f"  {tone} {s[:120].strip()}{'…' if len(s) > 120 else ''}")
    sent_block = "\n".join(sent_lines) if sent_lines else "  (no sentences)"

    header = f'"{context_label}" — ' if context_label else ""
    report = textwrap.dedent(f"""\
        ## Sentiment Analysis {emoji}
        {header}

        | Metric        | Value                        |
        |---------------|------------------------------|
        | Label         | **{label}**                  |
        | Polarity      | `{polarity:+.3f}` (−1 → +1)  |
        | Confidence    | `{confidence}%`              |
        | Positive hits | {pos_score:.1f} pts          |
        | Negative hits | {neg_score:.1f} pts          |
        | Words scanned | {n}                          |

        ### Top Positive Keywords
        {", ".join(f"`{w}`" for w in top_pos) if top_pos else "_none detected_"}

        ### Top Negative Keywords
        {", ".join(f"`{w}`" for w in top_neg) if top_neg else "_none detected_"}

        ### Sentence-Level Tone  (⊕ positive · ⊖ negative · ○ neutral)
        {sent_block}
    """)
    return [types.TextContent(type="text", text=report)]


# ═══════════════════════════════════════════════════════════════════════════════
# Part 2 — Tool 2: assess_source_credibility
# ═══════════════════════════════════════════════════════════════════════════════

def _assess_source_credibility(args: dict) -> list[types.TextContent]:
    """
    Heuristic credibility scoring for a web source.

    Signals evaluated (each adds/subtracts from a 0-100 base score of 50):
      +25  Known credible domain (academic, major news, gov)
      +15  Credible TLD (.edu, .gov, .org, .ac.xx)
      +10  URL contains no sensational path words
      +10  Snippet length ≥ 200 chars (substantive content)
      +10  Snippet has ≥ 2 numeric facts (dates, %, measurements)
      −20  URL or title contains clickbait/sensational signals
      −15  URL has excessive query params or tracking tokens
      −10  Very short snippet (< 50 chars) — content unclear
      −5   Domain is an IP address
    """
    url     = args.get("url",     "").strip()
    snippet = args.get("snippet", "").strip()
    title   = args.get("title",   "").strip()

    if not url:
        return [types.TextContent(type="text", text="ERROR: url is required")]

    score   = 50
    signals = []

    # Parse domain
    domain_match = re.search(r'https?://(?:www\.)?([^/?\s]+)', url)
    domain       = domain_match.group(1).lower() if domain_match else ""

    # ── Positive signals ──────────────────────────────────────────────────────
    if any(domain == d or domain.endswith("." + d) for d in _CREDIBLE_DOMAINS):
        score += 25
        signals.append(("✅", f"Known credible domain: {domain}", +25))

    matched_tld = next((t for t in _CREDIBLE_TLDS if domain.endswith(t)), None)
    if matched_tld and ("✅" not in [s[0] for s in signals]):  # avoid double-counting
        score += 15
        signals.append(("✅", f"Credible TLD: {matched_tld}", +15))
    elif matched_tld:
        signals.append(("✅", f"Credible TLD: {matched_tld}", 0))

    path = url.split("?")[0].lower()
    if not any(w in path for w in _LOW_CRED_SIGNALS):
        score += 10
        signals.append(("✅", "URL path contains no sensational keywords", +10))

    if len(snippet) >= 200:
        score += 10
        signals.append(("✅", f"Substantive snippet ({len(snippet)} chars)", +10))

    numeric_facts = len(re.findall(r'\d+(?:\.\d+)?(?:\s*%|\s*°|\s*km|\s*kg|\s*GB)?', snippet))
    if numeric_facts >= 2:
        score += 10
        signals.append(("✅", f"Contains {numeric_facts} numeric facts/measurements", +10))

    # ── Negative signals ──────────────────────────────────────────────────────
    combined_text = (url + " " + title + " " + snippet).lower()
    clickbait_found = [w for w in _LOW_CRED_SIGNALS if w in combined_text]
    if clickbait_found:
        score -= 20
        signals.append(("⚠️", f"Sensational/clickbait signals: {clickbait_found}", -20))

    query_params = url.count("&") + url.count("utm_")
    if query_params >= 3:
        score -= 15
        signals.append(("⚠️", f"Excessive tracking parameters ({query_params})", -15))

    if snippet and len(snippet) < 50:
        score -= 10
        signals.append(("⚠️", "Very short snippet — content quality unclear", -10))

    if re.match(r'\d{1,3}(\.\d{1,3}){3}', domain):
        score -= 5
        signals.append(("⚠️", "Domain is a raw IP address", -5))

    # Clamp
    score = max(0, min(100, score))

    # Tier
    if score >= 70:
        tier, tier_emoji = "High",   "🟢"
    elif score >= 40:
        tier, tier_emoji = "Medium", "🟡"
    else:
        tier, tier_emoji = "Low",    "🔴"

    # Bar
    bar_filled = round(score / 5)
    bar        = "█" * bar_filled + "░" * (20 - bar_filled)

    signal_rows = "\n".join(
        f"| {s[0]} | {s[1]} | {'+' if s[2] > 0 else ''}{s[2]} |"
        for s in signals
    )

    report = textwrap.dedent(f"""\
        ## Source Credibility Assessment {tier_emoji}

        **URL:** {url}
        {"**Title:** " + title if title else ""}

        | Metric    | Value                  |
        |-----------|------------------------|
        | Score     | **{score} / 100**      |
        | Tier      | **{tier}**  {tier_emoji}|
        | Verdict   | {"Recommended for use" if tier == "High" else "Use with caution" if tier == "Medium" else "Avoid or verify independently"} |

        `[{bar}]  {score}%`

        ### Scoring Signals

        | Signal | Description | Δ Score |
        |--------|-------------|---------|
        {signal_rows if signal_rows else "| — | No signals triggered | 0 |"}
    """)
    return [types.TextContent(type="text", text=report)]


# ═══════════════════════════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
