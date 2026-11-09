import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_DIR = ROOT / "automation" / "pipeline"

# Peak US Eastern viewing hours translated to UTC:
# Slot 1: 12:00 PM EST -> 17:00 UTC
# Slot 2: 6:00 PM EST  -> 23:00 UTC

def get_target_slots(now_utc=None):
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)

    slots = []
    # 2-day buffer: today, tomorrow, day after
    for day_offset in [0, 1, 2]:
        target_date = (now_utc + timedelta(days=day_offset)).date()
        times = [(17, 0), (23, 0)] # 12:00 PM ET & 6:00 PM ET

        for i, (hour, minute) in enumerate(times, 1):
            slot_dt = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=timezone.utc)
            if slot_dt > now_utc + timedelta(minutes=15):
                slot_id = f"{target_date.strftime('%Y-%m-%d')}_slot{i}"
                slots.append({
                    "id": slot_id,
                    "date": str(target_date),
                    "slot_num": i,
                    "iso": slot_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "dt": slot_dt
                })

    return slots

def build_topic_package(topic, slot):
    date_str = slot["date"]
    slot_dir = ROOT / "publish-queue" / date_str / f"{slot['id']}_{topic['id']}"
    slot_dir.mkdir(parents=True, exist_ok=True)

    # 1. Write verbatim script
    script_content = f"""# Script: {topic['title']}

**Slot**: {slot['id']} ({slot['iso']})  
**Style**: {topic['style']}  
**Channel**: @WhereMyDollarGo  

### Spoken Narration
"{topic['hook']}"

### Data Breakdown:
{json.dumps(topic.get('breakdown', {}), indent=2)}

### Key Takeaway:
"{topic.get('takeaway', '')}"

### Disclaimer:
"{topic.get('disclaimer', 'General education, not financial, tax, or legal advice.')}"
"""
    with open(slot_dir / "script.md", "w", encoding="utf-8") as f:
        f.write(script_content)

    # 2. Write metadata & description
    desc_content = f"""{topic['title']}

{topic['hook']}

Key Takeaways:
{topic.get('takeaway', '')}

Subscribe to @WhereMyDollarGo for daily breakdowns of money, taxes, and debt.

---
Disclaimer: {topic.get('disclaimer', 'General education, not financial advice.')}
"""
    with open(slot_dir / "metadata.md", "w", encoding="utf-8") as f:
        f.write(desc_content)

    print(f"Generated staging package for {topic['id']} at {slot_dir}")
    return slot_dir

def maintain_schedule_buffer(max_to_process=1):
    topics_file = PIPELINE_DIR / "topics.json"
    state_file = PIPELINE_DIR / "state.json"

    with open(topics_file, encoding="utf-8") as f:
        topics_data = json.load(f)
    topics = topics_data["topics"]

    state = {
        "channel_handle": "@WhereMyDollarGo",
        "next_topic_index": 0,
        "scheduled_slots": {},
        "weekly_history": []
    }
    if state_file.exists():
        try:
            with open(state_file, encoding="utf-8") as f:
                state = json.load(f)
        except Exception:
            pass

    scheduled_slots = state.get("scheduled_slots", {})
    next_idx = state.get("next_topic_index", 0)

    target_slots = get_target_slots()
    print(f"\n==========================================")
    print(f"Target Slots for 2-Day Buffer:")
    for s in target_slots:
        status = "SCHEDULED" if s["id"] in scheduled_slots else "MISSING"
        print(f"  [{status}] {s['id']} -> {s['iso']}")
    print(f"==========================================\n")

    unfilled = [s for s in target_slots if s["id"] not in scheduled_slots]
    if not unfilled:
        print("Buffer is full! All upcoming 2-day slots are prepared.")
        return

    # Also make sure daily carousel is generated
    try:
        from daily_carousel import generate_daily_carousel
        generate_daily_carousel()
    except Exception as e:
        print(f"Daily carousel notice: {e}")

    from uploader import upload_to_youtube

    to_process = unfilled[:max_to_process]
    print(f"Processing {len(to_process)} slot(s)...")

    for slot in to_process:
        topic = topics[next_idx % len(topics)]
        next_idx += 1

        print(f"\n--- Staging Slot: {slot['id']} ({slot['iso']}) ---")
        print(f"Topic: {topic['title']} [{topic['style']}]")

        pkg_dir = build_topic_package(topic, slot)

        # Upload if video exists and YouTube credentials are provided
        rendered_mp4 = pkg_dir / "video.mp4"
        yt_id = None
        if rendered_mp4.exists():
            yt_id = upload_to_youtube(
                str(rendered_mp4),
                topic["title"],
                topic["hook"],
                topic.get("tags", []),
                publish_at_iso=slot["iso"]
            )

        scheduled_slots[slot["id"]] = {
            "topic_id": topic["id"],
            "title": topic["title"],
            "style": topic["style"],
            "publish_at": slot["iso"],
            "youtube_id": yt_id,
            "status": "PUBLISHED" if yt_id else "STAGED",
            "scheduled_at": datetime.now(timezone.utc).isoformat()
        }

        # Update state
        state["next_topic_index"] = next_idx
        state["scheduled_slots"] = scheduled_slots
        state["last_run_utc"] = datetime.now(timezone.utc).isoformat()

        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

        # Log into styles-used.md
        styles_file = ROOT / "styles-used.md"
        with open(styles_file, "a", encoding="utf-8") as f:
            f.write(f"| Auto | {slot['date']} | {topic['title']} | {topic['style']} | 9:16 (Short) | Staged |\n")

    print("\nBuffer maintenance complete. State updated.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    maintain_schedule_buffer(max_to_process=count)
