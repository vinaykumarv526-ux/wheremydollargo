import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PIPELINE_DIR = ROOT / "automation" / "pipeline"

# ==============================================================================
# US AUDIENCE PEAK VIEWING TIMINGS (Target: US Working Adults 22-45)
# Times in US Eastern Time (ET) mapped to UTC:
#
# Slot 1 (Midday / Lunch Break Peak):
#   - US Eastern: 12:30 PM ET (Peak mobile usage during lunch)
#   - UTC: 17:30 UTC
#   - India (IST): 23:00 IST
#
# Slot 2 (Prime Evening / Post-Work Commute Peak):
#   - US Eastern: 6:30 PM ET (Peak home commute & evening wind-down)
#   - UTC: 23:30 UTC
#   - India (IST): 05:00 IST (next morning)
#
# Daily Carousel (Morning Commute Briefing):
#   - US Eastern: 8:00 AM ET (13:00 UTC / 18:30 IST)
#
# Saturday Long-Form Deep Dive:
#   - US Eastern: 10:30 AM ET (15:30 UTC / 21:00 IST)
# ==============================================================================

def get_target_slots(now_utc=None):
    if now_utc is None:
        now_utc = datetime.now(timezone.utc)

    slots = []
    # 2-day buffer: today, tomorrow, day after tomorrow
    for day_offset in [0, 1, 2]:
        target_date = (now_utc + timedelta(days=day_offset)).date()
        
        # Midday lunch peak (17:30 UTC = 12:30 PM ET) and Evening prime peak (23:30 UTC = 6:30 PM ET)
        times = [
            (17, 30, "Midday_Lunch_Peak_1230ET"),
            (23, 30, "Evening_Prime_Peak_1830ET")
        ]

        for i, (hour, minute, label) in enumerate(times, 1):
            slot_dt = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=timezone.utc)
            # Only keep slots in the future (at least 15 min from now)
            if slot_dt > now_utc + timedelta(minutes=15):
                slot_id = f"{target_date.strftime('%Y-%m-%d')}_slot{i}_{label}"
                slots.append({
                    "id": slot_id,
                    "date": str(target_date),
                    "slot_num": i,
                    "label": label,
                    "iso": slot_dt.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "dt": slot_dt
                })

    return slots

def build_topic_package(topic, slot):
    date_str = slot["date"]
    slot_dir = ROOT / "publish-queue" / date_str / f"{slot['id']}_{topic['id']}"
    slot_dir.mkdir(parents=True, exist_ok=True)

    style_name = topic.get("style", "Animated Explainer")
    hook_text = topic.get("hook", "")
    script_text = topic.get("script", hook_text)

    # 1. Write verbatim script
    script_content = f"""# Script: {topic['title']}

**Slot**: {slot['id']}
**Scheduled Peak Time**: {slot['iso']} (US Peak Hours)
**Style**: {style_name}  
**Channel**: @WhereMyDollarGo  

### Spoken Narration
"{script_text}"

### Data Breakdown:
{json.dumps(topic.get('breakdown', topic.get('scenes', {})), indent=2)}

### Key Takeaway:
"{topic.get('takeaway', '')}"

### Legal Disclaimer:
"{topic.get('disclaimer', 'General education, not financial, tax, or legal advice.')}"
"""
    with open(slot_dir / "script.md", "w", encoding="utf-8") as f:
        f.write(script_content)

    # 2. Write metadata & description
    desc_content = f"""{topic['title']}

{script_text}

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
    print(f"Target US Peak Slots for 2-Day Buffer:")
    for s in target_slots:
        status = "SCHEDULED" if s["id"] in scheduled_slots else "MISSING"
        print(f"  [{status}] {s['id']} -> {s['iso']}")
    print(f"==========================================\n")

    unfilled = [s for s in target_slots if s["id"] not in scheduled_slots]
    if not unfilled:
        print("Buffer is full! All upcoming 2-day peak slots are prepared.")
        return

    # Run daily carousel generation
    try:
        from daily_carousel import generate_daily_carousel
        generate_daily_carousel()
    except Exception as e:
        print(f"Daily carousel notice: {e}")

    from uploader import upload_to_youtube

    to_process = unfilled[:max_to_process]
    print(f"Processing {len(to_process)} peak slot(s)...")

    for slot in to_process:
        topic = topics[next_idx % len(topics)]
        next_idx += 1

        style_name = topic.get("style", "Animated Explainer")
        print(f"\n--- Staging Peak Slot: {slot['id']} ({slot['iso']}) ---")
        print(f"Topic: {topic['title']} [{style_name}]")

        pkg_dir = build_topic_package(topic, slot)

        rendered_mp4 = pkg_dir / "video.mp4"
        yt_id = None

        # Autonomously render video if scenes and script exist
        if not rendered_mp4.exists() and "scenes" in topic:
            try:
                import sys
                import shutil
                sys.path.append(str(ROOT / "automation"))
                if topic.get("id") == "explainer_000_how_money_works_stickman" or topic.get("style") == "Stickman Explainer":
                    from stickman_engine import produce_stickman_explainer_video
                    print(f"Autonomously rendering Stickonomics explainer video for {topic['id']}...")
                    stickman_out, _ = produce_stickman_explainer_video()
                    shutil.copy(str(stickman_out), str(rendered_mp4))
                else:
                    from video_engine import render_short_video
                    print(f"Autonomously rendering video for {topic['id']}...")
                    render_short_video(
                        topic_id=f"{slot['id']}_{topic['id']}",
                        script_text=topic.get("script", topic.get("hook", "")),
                        scenes_spec=topic["scenes"],
                        output_mp4=rendered_mp4
                    )
            except Exception as e:
                print(f"Autonomous video render notice: {e}")

        if rendered_mp4.exists():
            yt_id = upload_to_youtube(
                str(rendered_mp4),
                topic["title"],
                topic.get("script", topic.get("hook", "")),
                topic.get("tags", []),
                publish_at_iso=slot["iso"]
            )

        scheduled_slots[slot["id"]] = {
            "topic_id": topic["id"],
            "title": topic["title"],
            "style": style_name,
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
            f.write(f"| Auto | {slot['date']} | {topic['title']} | {style_name} | 9:16 (Short) | Staged Peak |\n")

    print("\nBuffer maintenance complete. State updated with US peak timings.")

if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    maintain_schedule_buffer(max_to_process=count)
