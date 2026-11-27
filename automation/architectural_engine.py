"""2D Flat Architectural Explainer Engine (1080x1920) Bridge
Orchestrates script generation, voice alignment, bespoke Canvas 2D kit & shot controller,
headless Chrome frame capture, procedural SFX soundtrack mix, and FFmpeg encoding.
"""
import json, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENGINE_DIR = ROOT / "automation" / "engine_inside_out"

def render_architectural_video(topic_spec, output_mp4):
    """Renders a complete 1080x1920 30fps architectural explainer reel.
    Strictly adheres to:
      - 9-cut viral retention narrative formula
      - Exact signature palette (#F4F1EA, #0E1A2B, #1A1A1E, #38BDF8, #FFD43B, #EF4444, #10B981)
      - Upper safe zone diagrams (y: 650-850), lower safe zone captions (y: 1250-1650)
      - Headless Chrome frame-exact capture + FFmpeg pipe
      - Procedural SFX + ducked curiosity bed
    """
    output_mp4 = Path(output_mp4).resolve()
    output_mp4.parent.mkdir(parents=True, exist_ok=True)
    
    topic_id = topic_spec.get("id", "explainer")
    print(f"\n[Architectural Engine] Rendering topic: {topic_spec.get('title', topic_id)}...")
    
    # Check if a custom script already exists or generate from topic specification
    script_path = ENGINE_DIR / "script.json"
    
    # 1. Voice synthesis and word alignment
    print("[1/4] Synthesizing voiceover and computing word-by-word timestamps...")
    res = subprocess.run(
        [sys.executable, str(ENGINE_DIR / "tools" / "voice_align.py"), str(ENGINE_DIR)],
        capture_output=True, text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"voice_align.py failed:\n{res.stderr}\n{res.stdout}")
    print(res.stdout.strip())
    
    # 2. Extract audio cues and generate procedural soundtrack mix
    print("[2/4] Generating procedural sound cues (whoosh, pop, slam, ding) & curiosity bed...")
    res_cues = subprocess.run(
        ["node", str(ENGINE_DIR / "tools" / "capture.mjs"), "cues"],
        cwd=str(ENGINE_DIR), capture_output=True, text=True
    )
    if res_cues.returncode != 0:
        raise RuntimeError(f"capture.mjs cues failed:\n{res_cues.stderr}\n{res_cues.stdout}")
        
    res_mix = subprocess.run(
        [sys.executable, str(ENGINE_DIR / "tools" / "mix.py"), str(ENGINE_DIR)],
        capture_output=True, text=True
    )
    if res_mix.returncode != 0:
        raise RuntimeError(f"mix.py failed:\n{res_mix.stderr}\n{res_mix.stdout}")
    print(res_mix.stdout.strip())
    
    # 3. Headless Chrome Frame Capture & FFmpeg Assembly
    print(f"[3/4] Capturing 1080x1920 30 FPS frames and encoding to {output_mp4}...")
    res_vid = subprocess.run(
        ["node", str(ENGINE_DIR / "tools" / "capture.mjs"), "video", str(output_mp4)],
        cwd=str(ENGINE_DIR), capture_output=True, text=True
    )
    if res_vid.returncode != 0:
        raise RuntimeError(f"capture.mjs video failed:\n{res_vid.stderr}\n{res_vid.stdout}")
    print(res_vid.stdout.strip())
    
    # 4. Generate High-Contrast Thumbnail
    thumb_path = output_mp4.parent / "thumbnail.jpg"
    print(f"[4/4] Generating high-contrast architectural thumbnail at {thumb_path}...")
    try:
        from PIL import Image, ImageDraw, ImageFont
        # Export frame from Cut 4 or Cut 8
        frame_tmp = ENGINE_DIR / "review" / "frames" / "t14.00.jpg"
        if not frame_tmp.exists():
            subprocess.run(["node", str(ENGINE_DIR / "tools" / "capture.mjs"), "frames", "review/frames", "14.0"], cwd=str(ENGINE_DIR))
        
        if frame_tmp.exists():
            img = Image.open(str(frame_tmp))
            draw = ImageDraw.Draw(img)
            font_path = ENGINE_DIR / "fonts" / "Inter-Black.otf"
            try:
                font = ImageFont.truetype(str(font_path), 84)
            except Exception:
                font = ImageFont.load_default()
                
            title_text = topic_spec.get("title", "WHAT IS A TAX?").upper()
            if "(" in title_text:
                title_text = title_text.split("(")[0].strip()
            if len(title_text) > 24:
                title_text = title_text[:24] + "..."
                
            pill_w, pill_h = 880, 136
            px, py = (1080 - pill_w) // 2, 280
            draw.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=68, fill="#FFD43B", outline="#1A1A1E", width=8)
            bbox = draw.textbbox((0, 0), title_text, font=font)
            tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text((px + (pill_w - tw)//2, py + (pill_h - th)//2 - 8), title_text, font=font, fill="#1A1A1E")
            img.save(str(thumb_path), quality=95)
    except Exception as e:
        print(f"Notice on thumbnail generation: {e}")
        
    print(f"Successfully produced architectural explainer package at {output_mp4}")
    return output_mp4

if __name__ == "__main__":
    test_topic = {
        "id": "explainer_001_what_is_a_tax",
        "title": "What is a Tax?",
        "style": "2D Flat Architectural Explainer"
    }
    render_architectural_video(test_topic, ROOT / "renders" / "what_is_a_tax.mp4")
