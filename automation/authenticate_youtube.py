"""
Automated One-Time YouTube OAuth Authorization Helper for WhereMyDollarGo
"""
import os
import sys
import json
import webbrowser
import subprocess
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / "youtube_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def main():
    if not CLIENT_SECRET_FILE.exists():
        print(f"Error: {CLIENT_SECRET_FILE} does not exist", flush=True)
        sys.exit(1)

    with open(CLIENT_SECRET_FILE, "r", encoding="utf-8") as f:
        cs = json.load(f)

    app_info = cs.get("installed") or cs.get("web")
    client_id = app_info.get("client_id")
    client_secret = app_info.get("client_secret")

    print(f"Starting authentication for client_id: {client_id[:25]}...", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRET_FILE),
        scopes=SCOPES
    )

    # Use run_local_server which automatically opens the browser
    creds = flow.run_local_server(
        port=8080,
        prompt="consent",
        access_type="offline",
        open_browser=True
    )

    refresh_token = creds.refresh_token
    token_data = {
        "token": creds.token,
        "refresh_token": refresh_token,
        "token_uri": creds.token_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": creds.scopes
    }

    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)
    print(f"[OK] Saved token locally to {TOKEN_FILE}", flush=True)

    # Fetch channel name
    try:
        yt = build("youtube", "v3", credentials=creds)
        res = yt.channels().list(mine=True, part="snippet").execute()
        if res.get("items"):
            name = res["items"][0]["snippet"]["title"]
            print(f"[OK] Connected to YouTube channel: '{name}'", flush=True)
    except Exception as e:
        print(f"Channel fetch info: {e}", flush=True)

    # Automatically set GitHub Secrets
    if refresh_token:
        print("Uploading secrets to GitHub repository vinaykumarv526-ux/wheremydollargo...", flush=True)
        repo = "vinaykumarv526-ux/wheremydollargo"
        subprocess.run(["gh", "secret", "set", "YT_CLIENT_ID", "--body", client_id, "--repo", repo], check=True)
        subprocess.run(["gh", "secret", "set", "YT_CLIENT_SECRET", "--body", client_secret, "--repo", repo], check=True)
        subprocess.run(["gh", "secret", "set", "YT_REFRESH_TOKEN", "--body", refresh_token, "--repo", repo], check=True)
        print("[SUCCESS] All YouTube credentials stored in GitHub Secrets! 100% automated.", flush=True)

if __name__ == "__main__":
    main()
