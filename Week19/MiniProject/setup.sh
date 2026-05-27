#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Smart Research Scout — Setup Script
# Run once on a clean machine to install all dependencies.
# ─────────────────────────────────────────────────────────────────────────────
set -e

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║    Smart Research Scout — Setup           ║"
echo "╚═══════════════════════════════════════════╝"
echo ""

# ── 1. Python deps ────────────────────────────────────────────────────────────
echo "→ Installing Python dependencies…"
pip install -r requirements.txt --quiet

# ── 2. Node / npm ─────────────────────────────────────────────────────────────
if ! command -v node &>/dev/null; then
  echo "⚠  Node.js not found. Install from https://nodejs.org (v18+)"
  exit 1
fi
echo "→ Node.js: $(node --version)"

# ── 3. Third-party MCP servers ────────────────────────────────────────────────
echo "→ Installing @modelcontextprotocol/server-brave-search…"
npm install -g @modelcontextprotocol/server-brave-search --silent

echo "→ Installing @modelcontextprotocol/server-filesystem…"
npm install -g @modelcontextprotocol/server-filesystem --silent

# ── 4. Env file ───────────────────────────────────────────────────────────────
if [ ! -f .env ]; then
  cp .env.example .env
  echo ""
  echo "✅ Created .env from .env.example"
  echo "   → Edit .env and add your GROQ_API_KEY and BRAVE_API_KEY"
else
  echo "→ .env already exists — skipping"
fi

# ── 5. Directories ────────────────────────────────────────────────────────────
mkdir -p logs outputs

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Edit .env with your API keys"
echo "  2. Run:  streamlit run ui/app.py"
echo ""
