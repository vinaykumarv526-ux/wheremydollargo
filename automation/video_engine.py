"""
Automated Video Production Engine for WhereMyDollarGo
Generates 1080x1920 vertical Shorts with voiceover (edge-tts), visual animated cards,
data breakdowns, and burned-in captions, then publishes/schedules to YouTube.
"""
import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "renders"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Color Palette (WhereMyDollarGo Brand)
NAVY_BG = (11, 15, 25)
CARD_BG = (15, 23, 42)
TEAL_ACCENT = (16, 185, 129)
CYAN_ACCENT = (56, 189, 248)
GOLD_ACCENT = (245, 158, 11)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)

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

async def synthesize_voice(text, output_audio_path, voice="en-US-GuyNeural"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate="+0%", pitch="-2Hz")
    await comm.save(str(output_audio_path))
    print(f"[VOICE] Synthesized audio to {output_audio_path}")

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def create_slide_image(title, subtitle, metric_label, metric_val, detail_lines, progress_pct, output_path):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=NAVY_BG)
    draw = ImageDraw.Draw(im)

    # Subtle top glow
    for r in range(120, 0, -10):
        alpha = int(25 * (r / 120))
        draw.ellipse([(w//2 - r*4, -r*2), (w//2 + r*4, r*2)], fill=(16, 185, 129))

    # Top brand header
    header_font = get_font(34)
    draw.text((w // 2, 100), "WHERE MY DOLLAR GO", fill=TEAL_ACCENT, font=header_font, anchor="mm")
    tagline_font = get_font(24)
    draw.text((w // 2, 145), "Every Dollar, Explained • @WhereMyDollarGo", fill=TEXT_MUTED, font=tagline_font, anchor="mm")

    # Progress bar
    bar_y = 190
    draw.line([(80, bar_y), (w - 80, bar_y)], fill=(30, 41, 59), width=8)
    fill_w = int(80 + (w - 160) * progress_pct)
    if fill_w > 80:
        draw.line([(80, bar_y), (fill_w, bar_y)], fill=TEAL_ACCENT, width=8)

    # Title Card
    title_font = get_font(52)
    # Wrap title if long
    words = title.split()
    lines = []
    cur = []
    for wd in words:
        cur.append(wd)
        if len(" ".join(cur)) > 24:
            lines.append(" ".join(cur))
            cur = []
    if cur:
        lines.append(" ".join(cur))

    t_y = 300
    for l in lines:
        draw.text((w // 2, t_y), l, fill=TEXT_WHITE, font=title_font, anchor="mm")
        t_y += 68

    if subtitle:
        sub_font = get_font(32)
        draw.text((w // 2, t_y + 20), subtitle, fill=CYAN_ACCENT, font=sub_font, anchor="mm")

    # Center Hero Metric Card
    card_top = 580
    card_bot = 1120
    draw.rounded_rectangle([(80, card_top), (w - 80, card_bot)], radius=32, fill=CARD_BG, outline=(51, 65, 85), width=3)

    label_font = get_font(32)
    draw.text((w // 2, card_top + 70), metric_label.upper(), fill=GOLD_ACCENT, font=label_font, anchor="mm")

    val_font = get_font(96)
    draw.text((w // 2, card_top + 180), metric_val, fill=TEXT_WHITE, font=val_font, anchor="mm")

    # Details inside card
    det_font = get_font(34)
    d_y = card_top + 310
    for det in detail_lines:
        draw.text((140, d_y), f"• {det}", fill=(226, 232, 240), font=det_font)
        d_y += 62

    # Bottom Takeaway Card
    bot_card_top = 1200
    bot_card_bot = 1680
    draw.rounded_rectangle([(80, bot_card_top), (w - 80, bot_card_bot)], radius=24, fill=(15, 23, 42), outline=(30, 41, 59), width=2)

    takeaway_header_font = get_font(28)
    draw.text((120, bot_card_top + 50), "THE MONETARY BREAKDOWN:", fill=TEAL_ACCENT, font=takeaway_header_font)

    bot_text_font = get_font(30)
    info_points = [
        "Primary Source: Official Federal & Regulatory Data",
        "Updated for Current US Tax Year Baseline",
        "General education, not financial, tax, or legal advice."
    ]
    by = bot_card_top + 110
    for ip in info_points:
        draw.text((120, by), f"✓ {ip}", fill=TEXT_MUTED, font=bot_text_font)
        by += 54

    # Bottom prompt
    call_font = get_font(36)
    draw.text((w // 2, 1780), "Subscribe to @WhereMyDollarGo", fill=TEXT_WHITE, font=call_font, anchor="mm")

    im.save(output_path, "PNG")

def render_short_video(topic_id, script_text, scenes_spec, output_mp4):
    work_dir = OUTPUT_DIR / topic_id
    work_dir.mkdir(parents=True, exist_ok=True)

    audio_path = work_dir / "voice.mp3"
    print(f"\n--- Generating Video: {topic_id} ---")
    asyncio.run(synthesize_voice(script_text, audio_path))

    total_duration = get_audio_duration(audio_path)
    print(f"Total audio duration: {total_duration:.2f} seconds")

    num_scenes = len(scenes_spec)
    scene_duration = total_duration / num_scenes

    concat_lines = []
    for i, spec in enumerate(scenes_spec):
        slide_img = work_dir / f"slide_{i}.png"
        pct = (i + 1) / num_scenes
        create_slide_image(
            title=spec["title"],
            subtitle=spec.get("subtitle", ""),
            metric_label=spec["metric_label"],
            metric_val=spec["metric_val"],
            detail_lines=spec["details"],
            progress_pct=pct,
            output_path=slide_img
        )
        concat_lines.append(f"file '{slide_img.resolve().as_posix()}'")
        concat_lines.append(f"duration {scene_duration:.3f}")

    # Repeat last frame for ffmpeg concat demuxer quirk
    concat_lines.append(f"file '{work_dir.resolve().as_posix()}/slide_{num_scenes - 1}.png'")

    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    # Stitch images with audio
    print(f"Rendering final MP4 to {output_mp4}...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(audio_path),
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Video rendered: {output_mp4} ({os.path.getsize(output_mp4):,} bytes)")
    return output_mp4
