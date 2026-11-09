"""
Upload banner and update YouTube Channel Branding Settings directly via YouTube Data API v3
"""
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

ROOT = Path(__file__).resolve().parent.parent

def update_branding():
    token_file = ROOT / "youtube_token.json"
    banner_file = ROOT / "assets" / "banner.jpg"

    with open(token_file, "r", encoding="utf-8") as f:
        d = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=d.get("refresh_token"),
        token_uri="https://oauth2.googleapis.com/token",
        client_id=d.get("client_id"),
        client_secret=d.get("client_secret")
    )
    yt = build("youtube", "v3", credentials=creds)

    banner_url = None
    if banner_file.exists():
        print(f"Uploading banner from {banner_file} to YouTube...")
        try:
            media = MediaFileUpload(str(banner_file), mimetype="image/jpeg", resumable=True)
            banner_res = yt.channelBanners().insert(media_body=media).execute()
            banner_url = banner_res.get("url")
            print(f"[OK] Banner image uploaded! URL: {banner_url}")
        except Exception as e:
            print(f"[Notice] Banner upload response: {e}")

    # Fetch channel ID
    ch_info = yt.channels().list(mine=True, part="id,brandingSettings,snippet").execute()
    items = ch_info.get("items", [])
    if not items:
        print("Error: No channel found.")
        return

    channel_id = items[0]["id"]
    print(f"Updating branding settings for Channel ID: {channel_id} (@wheremydollargo)...")

    description = (
        "WhereMyDollarGo follows your money: taxes, banking, debt, and insurance explained in plain English.\n\n"
        "• Daily Shorts (12:30 PM ET & 6:30 PM ET)\n"
        "• Daily 'Last 24 Hours in Money' market brief (8:00 AM ET)\n"
        "• Saturday Deep-Dive documentary (10:30 AM ET)\n\n"
        "Every number and statistic is verified directly from official primary sources (IRS, Fed, BLS, SSA, EIA).\n\n"
        "General education, not financial, tax, legal, or insurance advice. Follow your dollar: @WhereMyDollarGo"
    )

    keywords = (
        "wheremydollargo \"where does my money go\" \"personal finance\" taxes fica "
        "banking \"interest rates\" insurance \"money breakdown\" inflation investing "
        "\"health insurance\" \"mortgage amortization\""
    )

    channel_branding = {
        "title": "WhereMyDollarGo",
        "description": description,
        "keywords": keywords,
        "defaultLanguage": "en"
    }

    body = {
        "id": channel_id,
        "brandingSettings": {
            "channel": channel_branding
        }
    }

    if banner_url:
        body["brandingSettings"]["image"] = {
            "bannerExternalUrl": banner_url
        }

    update_res = yt.channels().update(part="brandingSettings", body=body).execute()
    print("[SUCCESS] Channel branding updated successfully on YouTube!")
    print(json.dumps(update_res.get("brandingSettings"), indent=2))

if __name__ == "__main__":
    update_branding()
