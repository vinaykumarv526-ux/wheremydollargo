"""
Weekly Long-Form Deep Dive Producer & Scheduler for WhereMyDollarGo
Produces 16:9 widescreen (1920x1080) deep dive explainers every Saturday at 10:30 AM ET.
"""
import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = ROOT / "renders" / "weekly_long"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def get_font(size):
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "arialbd.ttf",
        "DejaVuSans-Bold.ttf",
    ]
    for p in font_candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None

async def synthesize_voice(text, output_audio_path):
    import edge_tts
    comm = edge_tts.Communicate(text, "en-US-GuyNeural", rate="+0%", pitch="-2Hz")
    await comm.save(str(output_audio_path))
    print(f"[VOICE] Synthesized long deep-dive audio to {output_audio_path}")

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_horizontal_slide(title, subtitle, metric_label, metric_val, detail_lines, takeaway, progress_pct, output_path):
    w, h = 1920, 1080
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)

    # Ambient top glow
    for r in range(180, 0, -12):
        draw.ellipse([(w//2 - r*5, -r*2), (w//2 + r*5, r*2)], fill=(16, 185, 129))

    # Top brand bar
    draw.text((100, 60), "WHERE MY DOLLAR GO  •  SATURDAY DEEP DIVE", fill=(16, 185, 129), font=get_font(28))
    draw.text((w - 100, 60), "@WhereMyDollarGo", fill=(148, 163, 184), font=get_font(24), anchor="ra")
    
    # Progress line
    bar_y = 110
    draw.line([(100, bar_y), (w - 100, bar_y)], fill=(30, 41, 59), width=6)
    fill_w = int(100 + (w - 200) * progress_pct)
    if fill_w > 100:
        draw.line([(100, bar_y), (fill_w, bar_y)], fill=(16, 185, 129), width=6)

    # Title & Subtitle (Left Header)
    draw.text((100, 180), title, fill=(255, 255, 255), font=get_font(52))
    if subtitle:
        draw.text((100, 250), subtitle, fill=(56, 189, 248), font=get_font(30))

    # Two-Column Layout
    # Column 1: Big Hero Metric Card (Left)
    col1_w = 640
    c1_left = 100
    c1_top = 330
    c1_bot = 880
    draw.rounded_rectangle([(c1_left, c1_top), (c1_left + col1_w, c1_bot)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
    draw.text((c1_left + col1_w // 2, c1_top + 80), metric_label.upper(), fill=(245, 158, 11), font=get_font(26), anchor="mm")
    draw.text((c1_left + col1_w // 2, c1_top + 200), metric_val, fill=(255, 255, 255), font=get_font(72), anchor="mm")
    
    # Bottom note in card 1
    draw.line([(c1_left + 40, c1_top + 320), (c1_left + col1_w - 40, c1_top + 320)], fill=(30, 41, 59), width=2)
    draw.text((c1_left + col1_w // 2, c1_top + 400), "Official Primary Data Source", fill=(100, 116, 139), font=get_font(22), anchor="mm")

    # Column 2: Detailed Breakdown & Analysis (Right)
    c2_left = c1_left + col1_w + 50
    c2_w = w - c2_left - 100
    draw.rounded_rectangle([(c2_left, c1_top), (c2_left + c2_w, c1_bot)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
    draw.text((c2_left + 50, c1_top + 60), "STEP-BY-STEP BREAKDOWN:", fill=(16, 185, 129), font=get_font(26))
    
    dy = c1_top + 130
    for det in detail_lines:
        draw.text((c2_left + 50, dy), f"• {det}", fill=(248, 250, 252), font=get_font(30))
        dy += 62

    # Takeaway banner inside column 2
    draw.rounded_rectangle([(c2_left + 40, c1_bot - 160), (c2_left + c2_w - 40, c1_bot - 40)], radius=16, fill=(30, 41, 59))
    draw.text((c2_left + 70, c1_bot - 110), f"Key Takeaway: {takeaway}", fill=(245, 158, 11), font=get_font(24))

    # Bottom legal footer
    draw.text((100, 960), "General education only. Not financial, tax, or legal advice.  •  Follow your money: @WhereMyDollarGo", fill=(100, 116, 139), font=get_font(22))
    
    im.save(output_path, "PNG")

def render_weekly_long_video(topic_id, script_text, scenes_spec, output_mp4):
    work_dir = OUTPUT_DIR / topic_id
    work_dir.mkdir(parents=True, exist_ok=True)

    audio_path = work_dir / "voice.mp3"
    print(f"\n--- [WEEKLY DEEP DIVE] Generating 16:9 Video: {topic_id} ---")
    asyncio.run(synthesize_voice(script_text, audio_path))

    total_duration = get_audio_duration(audio_path)
    print(f"Total audio duration: {total_duration:.2f} seconds")

    num_scenes = len(scenes_spec)
    scene_duration = total_duration / num_scenes

    concat_lines = []
    for i, spec in enumerate(scenes_spec):
        slide_img = work_dir / f"slide_{i}.png"
        pct = (i + 1) / num_scenes
        create_horizontal_slide(
            title=spec["title"],
            subtitle=spec.get("subtitle", ""),
            metric_label=spec["metric_label"],
            metric_val=spec["metric_val"],
            detail_lines=spec["details"],
            takeaway=spec.get("takeaway", "Follow your dollar with @WhereMyDollarGo"),
            progress_pct=pct,
            output_path=slide_img
        )
        concat_lines.append(f"file '{slide_img.resolve().as_posix()}'")
        concat_lines.append(f"duration {scene_duration:.3f}")

    concat_lines.append(f"file '{work_dir.resolve().as_posix()}/slide_{num_scenes - 1}.png'")

    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print(f"Rendering 16:9 Widescreen MP4 to {output_mp4}...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(audio_path),
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] 16:9 Deep Dive Rendered: {output_mp4} ({os.path.getsize(output_mp4):,} bytes)")
    return output_mp4

def schedule_saturday_deep_dive():
    # Long video script (~1.5 min deep dive)
    topic = {
        "id": "deep_dive_001_how_money_is_created",
        "title": "How Money is Actually Created (The Fractional Reserve System)",
        "script": (
            "Welcome to Dollar Trail's Saturday Deep Dive. Most people believe money is printed by the government on physical paper. "
            "In reality, over ninety percent of the money in the United States is created not by the government, but by commercial banks making loans. "
            "Here is the mechanism: when you deposit one thousand dollars into a bank, the bank does not lock that cash in a vault. "
            "Under fractional reserve principles, they hold a small liquidity buffer, and lend out nine hundred dollars to someone buying a car. "
            "That nine hundred dollars is deposited into the seller's account. Now, your bank balance says one thousand dollars, and the seller's balance says nine hundred dollars. "
            "Nineteen hundred dollars of spending power now exists from a single one thousand dollar seed. "
            "This cycle repeats across the entire financial system. Understanding how credit expands and contracts is the secret to understanding inflation, interest rates, and recessions. "
            "Subscribe to WhereMyDollarGo for every dollar explained."
        ),
        "scenes": [
            {
                "title": "How Money is Actually Created",
                "subtitle": "The Myth of the Money Printing Press",
                "metric_label": "Digital Bank Credit",
                "metric_val": "> 90% Digital",
                "details": [
                    "Most people believe government paper printing creates all money",
                    "Over 90% of US money supply exists purely as digital commercial bank credits",
                    "New money enters circulation whenever a commercial bank approves a loan"
                ],
                "takeaway": "Money is created through lending, not just printing presses."
            },
            {
                "title": "The Step-by-Step Multiplier Cycle",
                "subtitle": "How $1,000 Becomes $1,900 of Purchasing Power",
                "metric_label": "The Credit Multiplier",
                "metric_val": "1 Deposit = 2 Balances",
                "details": [
                    "Step 1: You deposit $1,000 in your checking account",
                    "Step 2: Bank holds a reserve buffer and lends $900 for an auto loan",
                    "Step 3: The borrower pays a seller, who deposits the $900 into their bank",
                    "Total recorded deposits in the economy now equal $1,900"
                ],
                "takeaway": "Both parties believe they have liquid cash at the exact same time."
            },
            {
                "title": "Why This Cycle Drives the Economy",
                "subtitle": "Credit Expansion vs Credit Contraction",
                "metric_label": "The Economic Engine",
                "metric_val": "Credit Flow",
                "details": [
                    "When loans are cheap and plentiful, money supply expands (booms & inflation)",
                    "When the Federal Reserve raises interest rates, borrowing slows down",
                    "When loans are paid back without new borrowing, money supply actually shrinks"
                ],
                "takeaway": "Interest rates are the brakes and accelerator of the money supply."
            },
            {
                "title": "The Golden Rule of Monetary Literacy",
                "subtitle": "Protecting Your Personal Wealth",
                "metric_label": "Core Summary",
                "metric_val": "Debt vs Real Assets",
                "details": [
                    "Holding paper dollars guarantees purchasing power loss over decades",
                    "True wealth is stored in productive businesses, real estate, and hard assets",
                    "General education only. Follow your money: @WhereMyDollarGo"
                ],
                "takeaway": "Own productive assets that benefit when credit expands."
            }
        ]
    }

    now_utc = datetime.now(timezone.utc)
    # Calculate upcoming Saturday 10:30 AM ET (15:30 UTC)
    days_until_sat = (5 - now_utc.weekday()) % 7
    if days_until_sat == 0 and now_utc.hour >= 15:
        days_until_sat = 7
    target_sat = (now_utc + timedelta(days=days_until_sat)).date()
    sat_iso = f"{target_sat}T15:30:00Z"

    mp4_path = OUTPUT_DIR / f"{topic['id']}.mp4"
    render_weekly_long_video(topic["id"], topic["script"], topic["scenes"], mp4_path)

    # Upload & Schedule
    sys.path.append(str(ROOT / "automation" / "pipeline"))
    try:
        from uploader import upload_to_youtube
    except ImportError:
        from pipeline.uploader import upload_to_youtube
    print(f"\n[YOUTUBE] Scheduling Saturday Deep Dive for {sat_iso}...")
    yt_id = upload_to_youtube(
        video_path=str(mp4_path),
        title=f"{topic['title']} (Full Deep Dive)",
        description=topic["script"] + "\n\nSubscribe to @WhereMyDollarGo for weekly Saturday deep dives into money and economics.",
        tags=["moneycreation", "fractionalreserve", "economics", "federalreserve", "banking", "wheremydollargo"],
        publish_at_iso=sat_iso
    )

    print(f"\n[SUCCESS] Saturday Deep Dive scheduled on YouTube! Video ID: {yt_id} (Release: {sat_iso})")
    return yt_id

if __name__ == "__main__":
    schedule_saturday_deep_dive()
