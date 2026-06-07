# AI Agent Remote 📱→💻

Control any AI agent from your phone. Send prompts from anywhere — your laptop keeps working.

## Supported Targets
- Cursor
- Claude (desktop)
- ChatGPT
- Codex
- Terminal

## Files
- server.py — Run this on your laptop
- phone-ui.html — Served automatically to your phone
- setup.sh — Run once on first setup

## Setup (5 minutes)

**1. Install cloudflared**
brew install cloudflared

**2. Start the server**
cd cursor-remote && python3 server.py

**3. Expose via Cloudflare Tunnel**
cloudflared tunnel run your-tunnel-name

**4. Open on your phone**
Visit your tunnel URL, enter token, connect — done.

## How It Works
Phone → Cloudflare Tunnel → server.py → Target App (paste + Enter)

## Token
Change via: CURSOR_REMOTE_TOKEN=my-token python3 server.py
