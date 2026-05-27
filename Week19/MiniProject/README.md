# 🔍 Smart Research Scout

An end-to-end agentic application that integrates two third-party MCP servers with a custom insights server, orchestrated by an LLM (Groq or Ollama) via a Streamlit UI.

## Architecture

```
User Goal (Streamlit UI)
        │
        ▼
  MCP Orchestrator (client/orchestrator.py)
        │
   LLM (Groq / Ollama) plans tool calls
        │
   ┌────┴──────────────┬────────────────────┐
   ▼                   ▼                    ▼
Brave Search MCP   Filesystem MCP     Custom Insights MCP
(web search)       (save/read files)  (summarize/cite)
```

## Third-Party MCP Servers Used

1. **`@modelcontextprotocol/server-brave-search`** — web search via Brave API
2. **`@modelcontextprotocol/server-filesystem`** — local file read/write

## Quick Start (clean machine)

### 1. Prerequisites
```bash
python3 -m pip install -r requirements.txt
npm install -g @modelcontextprotocol/server-brave-search
npm install -g @modelcontextprotocol/server-filesystem
```

### 2. Configure environment
```bash
cp .env.example .env
# Edit .env with your keys
```

### 3. Run
```bash
streamlit run ui/app.py
```

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (get at console.groq.com) |
| `BRAVE_API_KEY` | Brave Search API key (free tier available) |
| `LLM_BACKEND` | `groq` or `ollama` (default: `groq`) |
| `OLLAMA_BASE_URL` | Ollama endpoint (default: `http://localhost:11434`) |
| `OLLAMA_MODEL` | Model name for Ollama (default: `llama3`) |
| `OUTPUT_DIR` | Where to save research notes (default: `./outputs`) |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING` (default: `INFO`) |
