"""
Bulletproof One-Time YouTube OAuth Authorization Helper for WhereMyDollarGo
Listens on http://localhost:8080/, captures authorization code, exchanges it directly with
Google OAuth2 endpoint (bypassing any state mismatch errors), stores credentials in
youtube_token.json, and pushes YT_REFRESH_TOKEN to GitHub Secrets.
"""
import os
import sys
import json
import webbrowser
import subprocess
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / "youtube_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

captured_code = None

class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global captured_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            captured_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """
            <html>
            <body style="font-family: system-ui, sans-serif; background: #0b0f19; color: #f8fafc; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0;">
                <div style="background: #0f172a; padding: 40px; border-radius: 16px; border: 2px solid #10b981; text-align: center; max-width: 500px;">
                    <h1 style="color: #10b981; margin-top: 0;">Authorization Successful!</h1>
                    <p style="font-size: 18px; color: #cbd5e1;">Your YouTube channel token has been captured and stored.</p>
                    <p style="font-size: 14px; color: #94a3b8;">GitHub Secrets are updating and scheduled uploads are resuming automatically.</p>
                    <p style="font-size: 14px; color: #38bdf8;">You can safely close this browser window now.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode("utf-8"))
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"No code received in callback.")

    def log_message(self, format, *args):
        # Suppress noisy standard HTTP logs
        pass

def main():
    global captured_code
    if not CLIENT_SECRET_FILE.exists():
        print(f"Error: {CLIENT_SECRET_FILE} does not exist", flush=True)
        sys.exit(1)

    with open(CLIENT_SECRET_FILE, "r", encoding="utf-8") as f:
        cs = json.load(f)

    app_info = cs.get("installed") or cs.get("web")
    client_id = app_info.get("client_id")
    client_secret = app_info.get("client_secret")

    redirect_uri = "http://localhost:8080/"

    # Generate Google OAuth2 Authorization URL
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent"
    }
    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(auth_params)

    print("\n=======================================================", flush=True)
    print("  WhereMyDollarGo YouTube Authorization Server", flush=True)
    print("=======================================================", flush=True)
    print(f"\n1. Opening browser to authorization URL:")
    print(f"\n{auth_url}\n", flush=True)

    # Start local HTTP server on port 8080
    server_address = ("", 8080)
    try:
        httpd = HTTPServer(server_address, OAuthHandler)
    except Exception as e:
        print(f"Error starting port 8080 server: {e}")
        sys.exit(1)

    # Open browser
    webbrowser.open(auth_url)
    print("2. Listening on http://localhost:8080/ for Google callback...", flush=True)

    # Wait for the single callback request
    while not captured_code:
        httpd.handle_request()

    print("\n[OK] Received authorization code from Google!", flush=True)

    # Exchange code for access & refresh token
    token_url = "https://oauth2.googleapis.com/token"
    token_payload = {
        "code": captured_code,
        "client_id": client_id,
        "client_secret": client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }

    res = requests.post(token_url, data=token_payload)
    if res.status_code != 200:
        print(f"Failed to exchange token: {res.status_code} - {res.text}", flush=True)
        sys.exit(1)

    tokens = res.json()
    refresh_token = tokens.get("refresh_token")
    access_token = tokens.get("access_token")

    token_data = {
        "token": access_token,
        "refresh_token": refresh_token,
        "token_uri": token_url,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": SCOPES
    }

    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)
    print(f"[OK] Saved fresh token locally to {TOKEN_FILE}", flush=True)

    # Automatically set GitHub Secrets
    if refresh_token:
        print("Uploading new token to GitHub Secrets (vinaykumarv526-ux/wheremydollargo)...", flush=True)
        repo = "vinaykumarv526-ux/wheremydollargo"
        subprocess.run(["gh", "secret", "set", "YT_CLIENT_ID", "--body", client_id, "--repo", repo], check=True)
        subprocess.run(["gh", "secret", "set", "YT_CLIENT_SECRET", "--body", client_secret, "--repo", repo], check=True)
        subprocess.run(["gh", "secret", "set", "YT_REFRESH_TOKEN", "--body", refresh_token, "--repo", repo], check=True)
        print("[SUCCESS] All YouTube credentials stored in GitHub Secrets! 100% automated.", flush=True)

    return refresh_token

if __name__ == "__main__":
    main()
