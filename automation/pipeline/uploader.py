import os
import sys
import json
import requests
from datetime import datetime, timezone
from pathlib import Path

def upload_to_youtube(video_path, title, description, tags, publish_at_iso=None):
    schedule_text = f" (Scheduled for: {publish_at_iso})" if publish_at_iso else " (Publish immediately)"
    print(f"Uploading to YouTube: {title}{schedule_text}")

    refresh_token = os.environ.get("YT_REFRESH_TOKEN")
    client_id = os.environ.get("YT_CLIENT_ID")
    client_secret = os.environ.get("YT_CLIENT_SECRET")

    if not (refresh_token and client_id and client_secret):
        token_path = os.environ.get("YT_TOKEN_FILE", "youtube_token.json")
        if os.path.exists(token_path):
            with open(token_path) as f:
                data = json.load(f)
                refresh_token = data.get("refresh_token")
                client_id = data.get("client_id")
                client_secret = data.get("client_secret")

    if not (refresh_token and client_id and client_secret):
        print("Notice: No YouTube API secrets (YT_REFRESH_TOKEN) found.")
        print("Operating in Staging/Queue mode: Asset generated and queued in repository.")
        return None

    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret,
            scopes=["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]
        )

        youtube = build("youtube", "v3", credentials=creds)

        status_dict = {
            "selfDeclaredMadeForKids": False
        }

        if publish_at_iso:
            status_dict["privacyStatus"] = "private"
            status_dict["publishAt"] = publish_at_iso
        else:
            status_dict["privacyStatus"] = "public"

        body = {
            "snippet": {
                "title": f"{title} #shorts",
                "description": f"{description}\n\n#shorts #finance #money #wheremydollargo",
                "tags": tags + ["shorts", "finance", "money", "wheremydollargo"],
                "categoryId": "27"  # Education
            },
            "status": status_dict
        }

        media = MediaFileUpload(video_path, mimetype="video/mp4", resumable=True)
        request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        video_id = response.get("id")
        print(f"SUCCESS: Uploaded to YouTube! Video ID: {video_id}")
        return video_id
    except Exception as e:
        print(f"Error during YouTube API upload: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python uploader.py <video_path> [title] [description] [publish_at_iso]")
        sys.exit(1)

    vid = sys.argv[1]
    tit = sys.argv[2] if len(sys.argv) > 2 else "Where Does Your Money Go? #shorts"
    desc = sys.argv[3] if len(sys.argv) > 3 else "Every dollar, explained."
    pub_iso = sys.argv[4] if len(sys.argv) > 4 else None
    tags = ["finance", "money", "wheremydollargo"]

    upload_to_youtube(vid, tit, desc, tags, publish_at_iso=pub_iso)
