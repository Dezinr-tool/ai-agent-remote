# Cursor Remote 📱→💻

Phone se Cursor ko control karo. Kahin bhi baitho — prompt bhejo — laptop chalata rahe.

---

## Files

```
cursor-remote/
├── server.py      ← Laptop pe run karo
├── phone-ui.html  ← Automatically serve hota hai
├── setup.sh       ← Pehli baar run karo
└── README.md
```

---

## Setup (5 minutes)

### Step 1 — ngrok install karo (one time)
```bash
# macOS
brew install ngrok/ngrok/ngrok
ngrok config add-authtoken YOUR_NGROK_TOKEN

# Linux
snap install ngrok
```
ngrok free account: https://ngrok.com

### Step 2 — Server start karo
```bash
cd cursor-remote
python3 server.py
```

### Step 3 — ngrok tunnel kholo (new terminal tab)
```bash
ngrok http 7432
```
Tumhe ek URL milega: `https://abc123.ngrok-free.app`

### Step 4 — Phone mein open karo
1. `https://abc123.ngrok-free.app` open karo phone mein
2. Token enter karo: `ganesh-secret-2024`
3. Connect → Done!

---

## Token change karna ho to

```bash
CURSOR_REMOTE_TOKEN=mera-custom-token python3 server.py
```

---

## How it works

```
Phone → [ngrok tunnel] → server.py → clipboard → Cursor (Cmd+V)
```

- **Copy mode**: Clipboard mein aata hai, tum manually Cmd+V karo Cursor mein
- **Auto-paste mode**: Cursor window automatically focus hoti hai aur paste ho jaata hai (macOS only)

---

## Quick presets (phone UI mein built-in)

- 🔍 Review & audit current file
- ♻️ Refactor code
- 🧪 Write tests
- 🐛 Fix errors
- 🛡️ Error handling
- 📝 Add documentation

---

## Troubleshooting

**Connect nahi ho raha?**
- Server run ho raha hai? `python3 server.py` check karo
- ngrok URL sahi hai? `https://` wala URL use karo, `http://` nahi
- Token match ho raha hai?

**Auto-paste kaam nahi kar raha?**
- macOS: System Preferences → Privacy → Accessibility → Terminal allow karo
- Linux: `xdotool` install karo: `sudo apt install xdotool`
- Windows: Manual Cmd+V hi use karo (auto-paste Windows pe limited hai)

**ngrok URL har restart pe change ho jaata hai?**
- Free plan mein hoga. Ya toh fixed subdomain lo (ngrok paid) ya har baar naya URL copy karo.
