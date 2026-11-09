"""
One-Time YouTube OAuth Authorization Helper for WhereMyDollarGo
Reads client_secret.json, authorizes your YouTube channel in your browser,
saves youtube_token.json, and automatically syncs GitHub Secrets via GitHub CLI (gh).
"""
import os
import sys
import json
import subprocess
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
CLIENT_SECRET_FILE = ROOT / "client_secret.json"
TOKEN_FILE = ROOT / "youtube_token.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def authenticate_and_sync_secrets():
    if not CLIENT_SECRET_FILE.exists():
        print(f"Error: Could not find client_secret.json at {CLIENT_SECRET_FILE}")
        sys.exit(1)

    with open(CLIENT_SECRET_FILE, "r", encoding="utf-8") as f:
        cs_data = json.load(f)

    app_info = cs_data.get("installed") or cs_data.get("web")
    client_id = app_info.get("client_id")
    client_secret = app_info.get("client_secret")

    print("==================================================================", flush=True)
    print("  WhereMyDollarGo: YouTube Channel One-Time Cloud Authorization  ", flush=True)
    print("==================================================================", flush=True)
    print(f"Client ID: {client_id[:20]}...", flush=True)
    print("Launching browser for YouTube authorization...", flush=True)

    flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET_FILE), SCOPES)
    creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")

    refresh_token = creds.refresh_token
    if not refresh_token:
        print("Warning: Google did not return a refresh_token.")
        print("To force Google to return a refresh token, revoke access at myaccount.google.com/permissions and run again.")

    # Save to local token file (ignored by git)
    token_data = {
        "token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": creds.scopes
    }
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(token_data, f, indent=2)
    print(f"\n[OK] Saved local credentials to {TOKEN_FILE}")

    # Test the connection & fetch channel info
    try:
        yt = build("youtube", "v3", credentials=creds)
        res = yt.channels().list(mine=True, part="snippet").execute()
        items = res.get("items", [])
        if items:
            title = items[0]["snippet"]["title"]
            print(f"[OK] Successfully verified YouTube Channel: '{title}'")
        else:
            print("[Notice] Account authorized, but no primary channel found for this Google identity.")
    except Exception as e:
        print(f"[Notice] Channel verification call: {e}")

    # Automatically sync secrets to GitHub Repository
    if refresh_token:
        print("\nSyncing secrets directly to GitHub repository (vinaykumarv526-ux/wheremydollargo)...")
        repo = "vinaykumarv526-ux/wheremydollargo"
        try:
            subprocess.run(["gh", "secret", "set", "YT_CLIENT_ID", "--body", client_id, "--repo", repo], check=True)
            subprocess.run(["gh", "secret", "set", "YT_CLIENT_SECRET", "--body", client_secret, "--repo", repo], check=True)
            subprocess.run(["gh", "secret", "set", "YT_REFRESH_TOKEN", "--body", refresh_token, "--repo", repo], check=True)
            print("[SUCCESS] All 3 YouTube secrets successfully stored in GitHub Actions!")
            print("The cloud pipeline can now publish and schedule to YouTube 100% autonomously.")
        except Exception as e:
            print(f"Could not automatically run gh secret set: {e}")
            print("You can manually set them in your GitHub repo under Settings -> Secrets -> Actions.")

if __name__ == "__main__":
    authenticate_and_sync_secrets()
