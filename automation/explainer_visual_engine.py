"""
Next-Gen Animated Explainer Video Engine for WhereMyDollarGo
Builds rich visual metaphorical scenes that match narration word-by-word:
- Conversational human US voice (en-US-GuyNeural / en-US-AndrewNeural with broadcast EQ)
- Background music ducking (warm lo-fi / tech beat bed)
- Illustrated graphics matching the story (e.g. pizza shop, slicing pie, stock certificate, trading exchange)
- Animated kinetic karaoke captions with active word highlighting
"""
import os
import sys
import json
import math
import asyncio
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "renders" / "explainers_v2"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_FILE = ROOT / "assets" / "music" / "bg_music.wav"

FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/calibrib.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

async def synthesize_human_voice(text, voice="en-US-GuyNeural", out_path="voice_raw.mp3"):
    import edge_tts
    # Pacing: natural conversational speed with no artificial speedup
    comm = edge_tts.Communicate(text, voice, rate="+0%", pitch="-2Hz")
    await comm.save(str(out_path))

def master_voice_with_music(voice_path, output_audio_path, duration_sec):
    """
    Applies studio broadcast EQ to voice, loops music ducked at -22dB, and merges them.
    """
    filter_complex = (
        "[0:a]highpass=f=75,equalizer=f=120:t=q:w=1:g=3.5,equalizer=f=3200:t=q:w=1:g=2,volume=1.3[v];"
        "[1:a]volume=0.08[m];"
        "[v][m]amix=inputs=2:duration=first[out]"
    )
    cmd = [
        "ffmpeg", "-y",
        "-i", str(voice_path),
        "-stream_loop", "-1", "-i", str(MUSIC_FILE),
        "-filter_complex", filter_complex,
        "-map", "[out]",
        str(output_audio_path)
    ]
    subprocess.run(cmd, check=True)

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

# ==============================================================================
# ILLUSTRATED SCENE RENDERERS (MATCHING NARRATION VISUALLY)
# ==============================================================================

def draw_top_hud(draw, w, title_tag, progress_pct):
    # Brand bar
    draw.text((w // 2, 80), "WHERE MY DOLLAR GO", fill=(16, 185, 129), font=get_font(28), anchor="mm")
    draw.text((w // 2, 125), "Financial Literacy Explainer", fill=(148, 163, 184), font=get_font(22), anchor="mm")
    
    # Progress bar
    bar_y = 160
    draw.line([(80, bar_y), (w - 80, bar_y)], fill=(30, 41, 59), width=8)
    fill_w = int(80 + (w - 160) * progress_pct)
    if fill_w > 80:
        draw.line([(80, bar_y), (fill_w, bar_y)], fill=(16, 185, 129), width=8)

    # Big Scene Badge
    badge_w, badge_h = 700, 70
    bx = (w - badge_w) // 2
    draw.rounded_rectangle([(bx, 200), (bx + badge_w, 270)], radius=35, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    draw.text((w // 2, 235), title_tag.upper(), fill=(255, 255, 255), font=get_font(30), anchor="mm")

def draw_captions(draw, w, h, text, yellow_word=None):
    # Giant bold kinetic captions in the safe zone
    cy = 1420
    draw.rounded_rectangle([(80, cy - 60), (w - 80, cy + 80)], radius=28, fill=(0, 0, 0, 220), outline=(51, 65, 85), width=2)
    
    words = text.split()
    font = get_font(46)
    
    # Simple word layout centered
    full_str = " ".join(words)
    bbox = font.getbbox(full_str)
    tw = bbox[2] - bbox[0]
    start_x = (w - tw) // 2

    cur_x = start_x
    for wd in words:
        is_highlight = (yellow_word and wd.lower().strip(",.!?") == yellow_word.lower().strip(",.!?"))
        col = (250, 204, 21) if is_highlight else (255, 255, 255) # Electric yellow or crisp white
        draw.text((cur_x, cy), wd, fill=col, font=font, anchor="lm")
        wd_w = font.getbbox(wd + " ")[2] - font.getbbox(wd + " ")[0]
        cur_x += wd_w

def render_pizza_scene_1(out_path, caption_text, yellow_word):
    """Scene 1: You open a pizza shop"""
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "Step 1: You Open a Pizza Shop", 0.2)

    # Draw Storefront Awning (Red & White Stripes)
    ax, ay, aw, ah = 240, 340, 600, 120
    stripe_w = 60
    for i in range(10):
        col = (220, 38, 38) if i % 2 == 0 else (255, 255, 255)
        draw.rectangle([(ax + i * stripe_w, ay), (ax + (i+1) * stripe_w, ay + ah)], fill=col)
    draw.rectangle([(ax, ay + ah), (ax + aw, ay + ah + 20)], fill=(185, 28, 28))

    # Storefront Building
    draw.rounded_rectangle([(ax - 20, ay + ah + 20), (ax + aw + 20, 1050)], radius=16, fill=(30, 41, 59), outline=(71, 85, 105), width=4)
    # Store Sign
    draw.rounded_rectangle([(ax + 80, ay + ah + 50), (ax + aw - 80, ay + ah + 140)], radius=12, fill=(245, 158, 11))
    draw.text((w // 2, ay + ah + 95), "TONY'S PIZZA", fill=(15, 23, 42), font=get_font(42), anchor="mm")

    # Big steaming delicious Pizza in the window
    cx, cy, r = w // 2, 800, 180
    # Crust
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(217, 119, 6), outline=(180, 83, 9), width=8)
    # Cheese
    draw.ellipse([(cx - r + 16, cy - r + 16), (cx + r - 16, cy + r - 16)], fill=(251, 191, 36))
    # Pepperonis
    peps = [(-60, -50), (40, -70), (-20, 10), (70, 20), (-80, 50), (20, 80)]
    for px, py in peps:
        draw.ellipse([(cx + px - 25, cy + py - 25), (cx + px + 25, cy + py + 25)], fill=(185, 28, 28))

    # Floating Callout Badge
    draw.rounded_rectangle([(240, 1120), (840, 1240)], radius=20, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 1160), "100% OWNED BY YOU", fill=(16, 185, 129), font=get_font(32), anchor="mm")
    draw.text((w // 2, 1205), "A real business selling real pizza", fill=(203, 213, 225), font=get_font(24), anchor="mm")

    draw_captions(draw, w, h, caption_text, yellow_word)
    im.save(out_path, "PNG")

def render_pizza_scene_2(out_path, caption_text, yellow_word):
    """Scene 2: Expansion & Need $100,000 cash"""
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "Step 2: Business is Booming!", 0.4)

    # 10 Stores Expansion Map Grid
    draw.rounded_rectangle([(140, 340), (940, 820)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
    draw.text((w // 2, 400), "THE EXPANSION GOAL", fill=(245, 158, 11), font=get_font(28), anchor="mm")
    draw.text((w // 2, 455), "Open 10 New Locations", fill=(255, 255, 255), font=get_font(44), anchor="mm")

    # 10 Illustrated Store Icons
    for idx in range(10):
        row = idx // 5
        col = idx % 5
        ix = 230 + col * 140
        iy = 540 + row * 120
        draw.rounded_rectangle([(ix - 45, iy - 40), (ix + 45, iy + 40)], radius=12, fill=(30, 41, 59), outline=(16, 185, 129), width=2)
        draw.text((ix, iy), f"#{idx+1}", fill=(16, 185, 129), font=get_font(26), anchor="mm")

    # Big Cash Need Card
    draw.rounded_rectangle([(140, 870), (940, 1220)], radius=24, fill=(15, 23, 42), outline=(239, 68, 68), width=3)
    draw.text((w // 2, 940), "CASH NEEDED TO EXPAND:", fill=(239, 68, 68), font=get_font(28), anchor="mm")
    draw.text((w // 2, 1030), "$100,000", fill=(255, 255, 255), font=get_font(84), anchor="mm")
    draw.text((w // 2, 1140), "Too big for a single bank loan!", fill=(148, 163, 184), font=get_font(28), anchor="mm")

    draw_captions(draw, w, h, caption_text, yellow_word)
    im.save(out_path, "PNG")

def render_pizza_scene_3(out_path, caption_text, yellow_word):
    """Scene 3: Slicing the business into 8 pieces"""
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "Step 3: Slicing into Shares", 0.6)

    cx, cy, r = w // 2, 680, 260
    # Crust
    draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)], fill=(217, 119, 6), outline=(180, 83, 9), width=8)
    draw.ellipse([(cx - r + 20, cy - r + 20), (cx + r - 20, cy + r - 20)], fill=(251, 191, 36))

    # Draw 8 cut lines (4 cutting diameters)
    for angle in [0, 45, 90, 135]:
        rad = math.radians(angle)
        x1 = cx + int(r * math.cos(rad))
        y1 = cy + int(r * math.sin(rad))
        x2 = cx - int(r * math.cos(rad))
        y2 = cy - int(r * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill=(15, 23, 42), width=8)

    # 4 slices labeled $25,000 each
    draw.rounded_rectangle([(140, 1020), (940, 1260)], radius=24, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 1080), "EACH SLICE = 1 SHARE", fill=(16, 185, 129), font=get_font(36), anchor="mm")
    draw.text((w // 2, 1150), "Sell 4 Slices at $25,000 Each", fill=(255, 255, 255), font=get_font(42), anchor="mm")
    draw.text((w // 2, 1210), "= $100,000 Raised Instantly!", fill=(245, 158, 11), font=get_font(30), anchor="mm")

    draw_captions(draw, w, h, caption_text, yellow_word)
    im.save(out_path, "PNG")

def render_pizza_scene_4(out_path, caption_text, yellow_word):
    """Scene 4: Shares grow in value"""
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "Step 4: Your Slice Grows!", 0.8)

    # Illustrated Stock Certificate
    cx, cy = w // 2, 600
    cw, ch = 760, 460
    draw.rounded_rectangle([(cx - cw//2, cy - ch//2), (cx + cw//2, cy + ch//2)], radius=24, fill=(15, 23, 42), outline=(245, 158, 11), width=4)
    # Inner border
    draw.rounded_rectangle([(cx - cw//2 + 16, cy - ch//2 + 16), (cx + cw//2 - 16, cy + ch//2 - 16)], radius=16, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
    
    draw.text((cx, cy - 150), "OFFICIAL SHARE CERTIFICATE", fill=(245, 158, 11), font=get_font(26), anchor="mm")
    draw.text((cx, cy - 80), "TONY'S PIZZA INC.", fill=(255, 255, 255), font=get_font(46), anchor="mm")
    draw.text((cx, cy), "1 Common Share (12.5% Ownership)", fill=(56, 189, 248), font=get_font(28), anchor="mm")
    
    # Value rocket badge
    draw.rounded_rectangle([(cx - 260, cy + 60), (cx + 260, cy + 170)], radius=20, fill=(16, 185, 129))
    draw.text((cx, cy + 115), "$25,000 ➔ $50,000!", fill=(15, 23, 42), font=get_font(44), anchor="mm")

    # Big Profit Banner
    draw.rounded_rectangle([(140, 920), (940, 1220)], radius=24, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 980), "BUSINESS BOOMED (+100% RETURN)", fill=(16, 185, 129), font=get_font(30), anchor="mm")
    draw.text((w // 2, 1050), "Your Investors Just Doubled Their Money", fill=(255, 255, 255), font=get_font(36), anchor="mm")
    draw.text((w // 2, 1130), "Because they own a real piece of the profit", fill=(148, 163, 184), font=get_font(26), anchor="mm")

    draw_captions(draw, w, h, caption_text, yellow_word)
    im.save(out_path, "PNG")

def render_pizza_scene_5(out_path, caption_text, yellow_word):
    """Scene 5: The Stock Market is the Supermarket"""
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "The Grand Takeaway", 1.0)

    # Trading Floor Supermarket Card
    draw.rounded_rectangle([(140, 360), (940, 780)], radius=24, fill=(15, 23, 42), outline=(56, 189, 248), width=3)
    draw.text((w // 2, 430), "THE STOCK MARKET IS JUST:", fill=(56, 189, 248), font=get_font(28), anchor="mm")
    draw.text((w // 2, 510), "A Giant Digital Supermarket", fill=(255, 255, 255), font=get_font(46), anchor="mm")
    draw.text((w // 2, 590), "Where millions of people buy and sell", fill=(203, 213, 225), font=get_font(30), anchor="mm")
    draw.text((w // 2, 650), "slices of companies every single second.", fill=(203, 213, 225), font=get_font(30), anchor="mm")
    draw.text((w // 2, 720), "(Apple, Microsoft, Tesla, or Tony's Pizza)", fill=(245, 158, 11), font=get_font(24), anchor="mm")

    # Big Golden Takeaway Shield
    draw.rounded_rectangle([(140, 840), (940, 1240)], radius=24, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 910), "NEVER FORGET THIS TRUTH:", fill=(16, 185, 129), font=get_font(28), anchor="mm")
    draw.text((w // 2, 990), "A Stock Is Not A Lottery Ticket.", fill=(255, 255, 255), font=get_font(44), anchor="mm")
    draw.text((w // 2, 1070), "It Is A Real Slice Of A Real Business.", fill=(250, 204, 21), font=get_font(42), anchor="mm")
    draw.text((w // 2, 1160), "Subscribe to @WhereMyDollarGo", fill=(255, 255, 255), font=get_font(32), anchor="mm")

    draw_captions(draw, w, h, caption_text, yellow_word)
    im.save(out_path, "PNG")

def produce_dynamic_explainer():
    work_dir = OUTPUT_DIR / "what_is_stock_market"
    work_dir.mkdir(parents=True, exist_ok=True)
    raw_voice = work_dir / "voice_raw.mp3"
    mastered_audio = work_dir / "audio_mastered.wav"
    output_mp4 = ROOT / "renders" / "explainer_pizza_stock_market_v2.mp4"

    # Human-paced script with natural conversational pauses
    script = (
        "Imagine you open a small pizza shop with your best friend. "
        "Business is booming! But to open ten new stores, you need one hundred thousand dollars. "
        "Instead of taking a bank loan, you cut your business into eight equal slices, and sell four slices for twenty-five thousand dollars each. "
        "Those slices are called shares! If your pizza chain explodes with profit, each slice is now worth fifty thousand dollars! "
        "The Stock Market is simply the giant supermarket where people buy and sell those slices every day. "
        "Subscribe to WhereMyDollarGo for every dollar explained!"
    )

    print("==================================================================")
    print("  Building Next-Gen Illustrated Explainer: What is the Stock Market? ")
    print("==================================================================")
    
    print("\n1. Synthesizing natural conversational American host voice (en-US-GuyNeural)...")
    asyncio.run(synthesize_human_voice(script, voice="en-US-GuyNeural", out_path=raw_voice))
    duration = get_audio_duration(raw_voice)
    print(f"Audio duration: {duration:.2f} seconds")

    print("\n2. Applying broadcast audio mastering & ducked lo-fi background music...")
    master_voice_with_music(raw_voice, mastered_audio, duration)

    print("\n3. Generating visual metaphorical illustrations matching speech...")
    # 5 Key visual scenes matching the audio timeline
    scenes = [
        (render_pizza_scene_1, "You open a small pizza shop with your friend.", "pizza"),
        (render_pizza_scene_2, "To open 10 new stores, you need $100,000.", "$100,000"),
        (render_pizza_scene_3, "You cut your business into 8 equal slices called shares.", "slices"),
        (render_pizza_scene_4, "If profits boom, each slice is worth $50,000!", "$50,000"),
        (render_pizza_scene_5, "A stock is simply a slice of a real company.", "stock")
    ]

    scene_dur = duration / len(scenes)
    concat_lines = []
    for i, (renderer_func, caption, yword) in enumerate(scenes):
        img_file = work_dir / f"scene_{i}.png"
        renderer_func(img_file, caption, yword)
        concat_lines.append(f"file '{img_file.resolve().as_posix()}'")
        concat_lines.append(f"duration {scene_dur:.3f}")

    concat_lines.append(f"file '{(work_dir / f'scene_{len(scenes)-1}.png').resolve().as_posix()}'")
    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print(f"\n4. Assembling and encoding final 1080x1920 MP4 video...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-i", str(mastered_audio),
        "-vf", "fps=30,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(output_mp4)
    ]
    subprocess.run(cmd, check=True)
    print(f"[SUCCESS] Next-Gen Explainer Video Rendered: {output_mp4} ({os.path.getsize(output_mp4):,} bytes)")

    # Upload & Publish to YouTube
    print("\n5. Publishing directly to YouTube...")
    sys.path.append(str(ROOT / "automation" / "pipeline"))
    from uploader import upload_to_youtube
    yt_id = upload_to_youtube(
        video_path=str(output_mp4),
        title="What is the Stock Market? (The Pizza Analogy Explained)",
        description=script + "\n\nSubscribe to @WhereMyDollarGo for daily finance & economics explainers.",
        tags=["whatisthestockmarket", "stockmarketforbeginners", "pizzaanalogy", "investing", "wheremydollargo"],
        publish_at_iso=None # Publish immediately!
    )
    print(f"\n[ALL DONE] Live on YouTube: https://youtube.com/shorts/{yt_id}")
    return yt_id

if __name__ == "__main__":
    produce_dynamic_explainer()
