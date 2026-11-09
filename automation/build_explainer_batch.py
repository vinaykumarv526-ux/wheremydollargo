"""
Explainer Series Producer & Scheduler for WhereMyDollarGo
Builds foundational conceptual explainers:
- What is a Tax?
- What is the Stock Market?
- What is a Trade?
- How a Trade is Actually Done
"""
import os
import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from video_engine import render_short_video
from pipeline.uploader import upload_to_youtube

ROOT = Path(__file__).resolve().parent.parent

def run_explainer_batch():
    topics_file = ROOT / "automation" / "pipeline" / "topics.json"
    with open(topics_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    topics = data["topics"]

    now_utc = datetime.now(timezone.utc)

    # 4 Explainer Videos Schedule:
    # 1. What is a Tax? -> Publish NOW (Immediate)
    # 2. What is the Stock Market? -> Tomorrow Midday Peak 12:30 PM ET (17:30 UTC)
    # 3. What is a Trade? -> Tomorrow Prime Evening Peak 6:30 PM ET (23:30 UTC)
    # 4. How a Trade is Actually Done -> Day After Tomorrow Midday Peak (17:30 UTC)
    schedules = [
        None, # NOW
        (now_utc + timedelta(days=1)).strftime("%Y-%m-%d") + "T17:30:00Z",
        (now_utc + timedelta(days=1)).strftime("%Y-%m-%d") + "T23:30:00Z",
        (now_utc + timedelta(days=2)).strftime("%Y-%m-%d") + "T17:30:00Z"
    ]

    print("==================================================================")
    print("  WhereMyDollarGo: Generating Foundational Explainer Series Batch ")
    print("==================================================================")

    results = []
    for i, topic in enumerate(topics[:4]):
        sched = schedules[i]
        mp4_path = ROOT / "renders" / f"{topic['id']}.mp4"

        print(f"\n--- [EXPLAINER #{i+1}] {topic['title']} ---")
        render_short_video(
            topic_id=topic["id"],
            script_text=topic["script"],
            scenes_spec=topic["scenes"],
            output_mp4=mp4_path
        )

        sched_label = "NOW (Immediate)" if not sched else f"Scheduled: {sched}"
        print(f"[YOUTUBE] Uploading ({sched_label})...")
        yt_id = upload_to_youtube(
            video_path=str(mp4_path),
            title=topic["title"],
            description=topic["script"],
            tags=topic.get("tags", []),
            publish_at_iso=sched
        )

        results.append({
            "title": topic["title"],
            "schedule": sched_label,
            "youtube_id": yt_id
        })

    print("\n==================================================================")
    print("              EXPLAINER SERIES BATCH COMPLETE!                    ")
    print("==================================================================")
    for r in results:
        print(f"• {r['title']} -> {r['schedule']} (Video ID: {r['youtube_id']})")

if __name__ == "__main__":
    run_explainer_batch()
