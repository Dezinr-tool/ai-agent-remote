#!/usr/bin/env python3
"""
Cursor Remote — Laptop Server v2
Phone se command bhejo → registered window mein auto-paste + execute
"""

import json
import time
import threading
import subprocess
import platform
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from urllib.parse import urlparse

PORT = 7432
SECRET_TOKEN = os.environ.get("CURSOR_REMOTE_TOKEN", "ganesh-secret-2024")
MAX_HISTORY = 50

# State
command_history = []
registered_window = {"app": "Cursor", "label": "Cursor"}
lock = threading.Lock()

# ── App configs ───────────────────────────────────────────────────────────────
APP_CONFIGS = {
    "Cursor": {"name": "Cursor", "type": "native"},
    "Claude": {"name": "Claude", "type": "native"},
    "ChatGPT": {"name": "ChatGPT", "type": "native"},
    "Codex": {"name": "Terminal", "type": "native"},
    "Custom": {"name": "Custom", "type": "native"},
}

# ── Clipboard ─────────────────────────────────────────────────────────────────
def copy_to_clipboard(text):
    try:
        proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
        proc.communicate(text.encode("utf-8"))
        return True
    except Exception as e:
        print(f"[CLIPBOARD ERROR] {e}")
        return False

def show_notification(message):
    try:
        script = f'display notification "{message}" with title "Cursor Remote"'
        subprocess.run(["osascript", "-e", script], check=False)
    except:
        pass

def focus_app_and_paste(app_name):
    """Focus the registered app window and paste + Enter"""
    script = f'''
    tell application "{app_name}" to activate
    delay 0.6
    tell application "System Events"
        keystroke "v" using command down
        delay 0.3
        key code 36
    end tell
    '''
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode == 0:
            return True, "pasted"
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def get_open_apps():
    """Get list of currently open applications"""
    script = '''
    tell application "System Events"
        set appList to name of every application process whose background only is false
    end tell
    return appList
    '''
    try:
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
        if result.returncode == 0:
            apps = [a.strip() for a in result.stdout.strip().split(",") if a.strip()]
            return apps
    except:
        pass
    return ["Cursor", "Claude", "ChatGPT"]

# ── Process command ───────────────────────────────────────────────────────────
def process_command(command, target_app=None):
    timestamp = datetime.now().strftime("%H:%M:%S")
    app = target_app or registered_window.get("app", "Cursor")
    
    entry = {
        "id": int(time.time() * 1000),
        "command": command,
        "app": app,
        "timestamp": timestamp,
        "status": "pending"
    }
    
    copy_to_clipboard(command)
    time.sleep(0.2)
    
    success, msg = focus_app_and_paste(app)
    
    if success:
        entry["status"] = "executed"
        show_notification(f"✓ Sent to {app}")
        print(f"\n[{timestamp}] ✅ EXECUTED in {app}")
        print(f"{'─'*50}")
        print(command[:100])
        print(f"{'─'*50}")
    else:
        entry["status"] = "copied"
        show_notification(f"Copied — paste in {app}")
        print(f"[{timestamp}] 📋 Copied (manual paste needed): {msg[:50]}")
    
    with lock:
        command_history.insert(0, entry)
        if len(command_history) > MAX_HISTORY:
            command_history.pop()
    
    return entry

# ── HTTP Handler ──────────────────────────────────────────────────────────────
class RemoteHandler(BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass
    
    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-Token")
    
    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_cors()
        self.end_headers()
        self.wfile.write(body)
    
    def auth_check(self):
        return self.headers.get("X-Token", "") == SECRET_TOKEN
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors()
        self.end_headers()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path in ["/", "/ui"]:
            ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "phone-ui.html")
            if os.path.exists(ui_path):
                with open(ui_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", len(content))
                self.end_headers()
                self.wfile.write(content)
            else:
                self.send_json({"error": "phone-ui.html not found"}, 404)
            return
        
        if parsed.path == "/ping":
            self.send_json({
                "status": "online",
                "platform": platform.system(),
                "time": datetime.now().strftime("%H:%M:%S"),
                "registered_window": registered_window,
                "token_hint": SECRET_TOKEN[:4] + "****"
            })
            return
        
        if parsed.path == "/history":
            if not self.auth_check():
                self.send_json({"error": "unauthorized"}, 401)
                return
            with lock:
                self.send_json({"history": command_history})
            return
        
        if parsed.path == "/apps":
            if not self.auth_check():
                self.send_json({"error": "unauthorized"}, 401)
                return
            apps = get_open_apps()
            self.send_json({"apps": apps, "registered": registered_window})
            return
        
        self.send_json({"error": "not found"}, 404)
    
    def do_POST(self):
        if not self.auth_check():
            self.send_json({"error": "unauthorized"}, 401)
            return
        
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        
        try:
            data = json.loads(body) if body else {}
        except:
            data = {}
        
        if parsed.path == "/command":
            command = data.get("command", "").strip()
            target_app = data.get("app", None)
            
            if not command:
                self.send_json({"error": "empty command"}, 400)
                return
            
            entry = process_command(command, target_app)
            self.send_json({"success": True, "entry": entry})
            return
        
        if parsed.path == "/register":
            app = data.get("app", "Cursor")
            label = data.get("label", app)
            with lock:
                registered_window["app"] = app
                registered_window["label"] = label
            print(f"[REGISTER] Window set to: {app}")
            self.send_json({"success": True, "registered": registered_window})
            return
        
        if parsed.path == "/clear":
            with lock:
                command_history.clear()
            self.send_json({"success": True})
            return
        
        self.send_json({"error": "not found"}, 404)

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"""
╔══════════════════════════════════════════╗
║       CURSOR REMOTE v2 — LAPTOP          ║
╠══════════════════════════════════════════╣
║  Port  : {PORT}                            ║
║  Token : {SECRET_TOKEN[:8]}...                      ║
╚══════════════════════════════════════════╝
✅ Server running on port {PORT}
""")
    server = HTTPServer(("0.0.0.0", PORT), RemoteHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server stopped.")
        server.server_close()

if __name__ == "__main__":
    main()
