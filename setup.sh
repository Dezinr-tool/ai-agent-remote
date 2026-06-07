#!/bin/bash
# ═══════════════════════════════════════════════════════
#  Cursor Remote — One-Command Setup
#  Run this once: bash setup.sh
# ═══════════════════════════════════════════════════════

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     CURSOR REMOTE — SETUP STARTING       ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ── 1. Python check ──────────────────────────────────
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Install it first."
    exit 1
fi
echo "✅ Python3 found"

# ── 2. ngrok check ───────────────────────────────────
if ! command -v ngrok &> /dev/null; then
    echo ""
    echo "📦 ngrok not found. Install karo:"
    echo "   Mac:   brew install ngrok/ngrok/ngrok"
    echo "   Linux: snap install ngrok"
    echo "   Or: https://ngrok.com/download"
    echo ""
    echo "⚠️  ngrok account banana hoga (free) aur authtoken set karna hoga:"
    echo "   ngrok config add-authtoken YOUR_TOKEN"
    echo ""
else
    echo "✅ ngrok found"
fi

# ── 3. macOS: accessibility permission reminder ──────
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo ""
    echo "⚠️  macOS: Auto-paste ke liye accessibility permission chahiye"
    echo "   System Preferences → Privacy & Security → Accessibility"
    echo "   → Terminal (ya iTerm) ko allow karo"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  SETUP COMPLETE. Ab run karo:"
echo ""
echo "  1️⃣   python3 server.py"
echo "  2️⃣   ngrok http 7432     (new terminal tab)"
echo "  3️⃣   ngrok URL phone mein open karo"
echo "═══════════════════════════════════════════"
echo ""
