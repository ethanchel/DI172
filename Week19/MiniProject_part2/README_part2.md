# Mini-Project Part 2 — Custom MCP Server Extension

Extension of Part 1. Same pipeline, same external servers — two new non-trivial tools added to the custom `insights_server.py`.

## What was added

### Tool 1 — `analyze_sentiment`

Lexicon-based sentiment analysis on any text (article snippet, search result, research note).

**Input:** `text` (required), `context_label` (optional)

**Output:** sentiment label (Positive / Neutral / Negative), polarity score from −1.0 to +1.0, confidence %, top emotional keywords, and a sentence-level tone breakdown.

**How it works:** tokenises the text and slides a 3-word window to detect negations (`not efficient` → negative) and intensifiers (`very powerful` → weight ×1.5). Polarity is computed as `(pos − neg) / (pos + neg)`, confidence via `tanh`. No external API or library required.

---

### Tool 2 — `assess_source_credibility`

Heuristic credibility scoring (0–100) for a web source given its URL and an optional snippet.

**Input:** `url` (required), `snippet` (optional), `title` (optional)

**Output:** score 0–100, tier (High / Medium / Low), and a detailed list of signals that influenced the score.

**Scoring signals:**

| Signal | Δ Score |
|---|---|
| Known credible domain (arxiv.org, bbc.com, nature.com…) | +25 |
| Credible TLD (.edu, .gov, .org, .ac.xx) | +15 |
| No sensational keywords in URL path | +10 |
| Substantive snippet (≥ 200 chars) | +10 |
| ≥ 2 numeric facts in snippet | +10 |
| Clickbait/sensational signals detected | −20 |
| Excessive tracking parameters | −15 |
| Very short snippet (< 50 chars) | −10 |
| Raw IP address as domain | −5 |

---

## Updated orchestration workflow

The LLM is now instructed to follow this extended pipeline:

1. **brave-search** — 2–3 web queries on the topic
2. **insights__assess_source_credibility** — filter low-quality sources before summarising
3. **insights__summarize_text** — condense high/medium credibility results
4. **insights__analyze_sentiment** — gauge the tone of each summarised piece
5. **insights__extract_key_points** — bullet-point takeaways
6. **insights__format_citations** — APA-style references
7. **insights__merge_notes** — compile into one document
8. **filesystem__write_file** — save final note as `.md`

---

## Files changed vs Part 1

| File | Change |
|---|---|
| `mcp_servers/insights_server.py` | Added `analyze_sentiment` and `assess_source_credibility` tools |
| `client/orchestrator.py` | Updated system prompt to include new tools in the workflow |

## Setup

Same as Part 1 — no new dependencies. All new tools use Python standard library only.

```bash
# From Part 1 setup (already done)
streamlit run ui/app.py
```
