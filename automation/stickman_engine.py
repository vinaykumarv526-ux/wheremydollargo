"""
Stickman Financial Explainer Engine for WhereMyDollarGo
Matches the exact Stickonomics style (https://www.youtube.com/shorts/jR-Db1wsTkw):
- Clean crisp white background (1080x1920)
- Expressive vector stickman (big round head, expressive eyes/eyebrows, open mouth, suit tie)
- Visual props: red inflation zigzag arrows, hanging price tags (OLD $2 / NEW $5), coin stacks, cash notes
- Kinetic karaoke captions (bold uppercase with radiant yellow word highlight)
- Fast-paced, engaging conversational human narration + ducked music bed
"""
import os
import sys
import math
import json
import asyncio
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "renders" / "stickman_explainers"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MUSIC_FILE = ROOT / "assets" / "music" / "bg_music.wav"

def get_font(size, bold=True):
    font_candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
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

# ==============================================================================
# VECTOR STICKMAN DRAWING FUNCTIONS
# ==============================================================================

def draw_shadow(draw, x, y, rx=90, ry=20):
    draw.ellipse([(x - rx, y - ry), (x + rx, y + ry)], fill=(225, 231, 239))

def draw_stickman(draw, x, y, pose="pointing_right", emotion="surprised", scale=1.0):
    """
    Renders an expressive stickman at (x, y) where (x, y) is the ground anchor between feet.
    scale: 1.0 -> character height ~750px.
    """
    ink = (20, 24, 33)
    white = (255, 255, 255)
    red = (220, 38, 38)
    
    # Ground shadow
    draw_shadow(draw, x, y, int(110 * scale), int(22 * scale))

    # Proportions
    head_r = int(95 * scale)
    head_y = int(y - 600 * scale)
    head_x = x
    
    pelvis_y = int(y - 240 * scale)
    pelvis_x = x
    
    # Legs & Feet
    foot_l_x = int(x - 50 * scale)
    foot_r_x = int(x + 50 * scale)
    foot_y = y - int(10 * scale)
    
    # Draw Legs (stroke 10px)
    draw.line([(pelvis_x, pelvis_y), (foot_l_x, foot_y)], fill=ink, width=int(10 * scale))
    draw.line([(pelvis_x, pelvis_y), (foot_r_x, foot_y)], fill=ink, width=int(10 * scale))
    # Shoes
    draw.ellipse([(foot_l_x - int(25*scale), foot_y - int(10*scale)), (foot_l_x + int(20*scale), foot_y + int(10*scale))], fill=ink)
    draw.ellipse([(foot_r_x - int(15*scale), foot_y - int(10*scale)), (foot_r_x + int(30*scale), foot_y + int(10*scale))], fill=ink)

    # Spine line
    shoulder_y = head_y + head_r + int(15 * scale)
    draw.line([(head_x, head_y + head_r), (pelvis_x, pelvis_y)], fill=ink, width=int(11 * scale))

    # Vest / Suit Torso (clean black tapered silhouette)
    vest_pts = [
        (head_x - int(32 * scale), shoulder_y),
        (head_x + int(32 * scale), shoulder_y),
        (pelvis_x + int(16 * scale), pelvis_y - int(30 * scale)),
        (pelvis_x - int(16 * scale), pelvis_y - int(30 * scale))
    ]
    draw.polygon(vest_pts, fill=ink)

    # White collar shirt
    collar_pts = [
        (head_x - int(18 * scale), shoulder_y),
        (head_x, shoulder_y + int(26 * scale)),
        (head_x + int(18 * scale), shoulder_y)
    ]
    draw.polygon(collar_pts, fill=white)

    # Red Tie
    tie_pts = [
        (head_x - int(7 * scale), shoulder_y + int(14 * scale)),
        (head_x + int(7 * scale), shoulder_y + int(14 * scale)),
        (head_x + int(10 * scale), shoulder_y + int(125 * scale)),
        (head_x, shoulder_y + int(148 * scale)),
        (head_x - int(10 * scale), shoulder_y + int(125 * scale))
    ]
    draw.polygon(tie_pts, fill=red)

    # Arms & Poses
    if pose == "pointing_right":
        # Left arm on chest / heart in surprise
        elbow_l = (head_x - int(75 * scale), shoulder_y + int(80 * scale))
        hand_l = (head_x - int(10 * scale), shoulder_y + int(70 * scale))
        draw.line([(head_x - int(25 * scale), shoulder_y + int(15 * scale)), elbow_l], fill=ink, width=int(9 * scale))
        draw.line([elbow_l, hand_l], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_l[0]-12, hand_l[1]-12), (hand_l[0]+12, hand_l[1]+12)], fill=ink)

        # Right arm pointing forward/right
        elbow_r = (head_x + int(85 * scale), shoulder_y + int(30 * scale))
        hand_r = (head_x + int(195 * scale), shoulder_y - int(25 * scale))
        draw.line([(head_x + int(25 * scale), shoulder_y + int(15 * scale)), elbow_r], fill=ink, width=int(9 * scale))
        draw.line([elbow_r, hand_r], fill=ink, width=int(9 * scale))
        # Pointing index finger
        draw.ellipse([(hand_r[0]-10, hand_r[1]-10), (hand_r[0]+10, hand_r[1]+10)], fill=ink)
        draw.line([hand_r, (hand_r[0] + int(35 * scale), hand_r[1] - int(8 * scale))], fill=ink, width=int(7 * scale))

    elif pose == "holding_money":
        elbow_l = (head_x - int(80 * scale), shoulder_y + int(90 * scale))
        hand_l = (head_x - int(55 * scale), shoulder_y + int(60 * scale))
        draw.line([(head_x - int(25 * scale), shoulder_y + int(15 * scale)), elbow_l], fill=ink, width=int(9 * scale))
        draw.line([elbow_l, hand_l], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_l[0]-12, hand_l[1]-12), (hand_l[0]+12, hand_l[1]+12)], fill=ink)

        elbow_r = (head_x + int(80 * scale), shoulder_y + int(90 * scale))
        hand_r = (head_x + int(55 * scale), shoulder_y + int(60 * scale))
        draw.line([(head_x + int(25 * scale), shoulder_y + int(15 * scale)), elbow_r], fill=ink, width=int(9 * scale))
        draw.line([elbow_r, hand_r], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_r[0]-12, hand_r[1]-12), (hand_r[0]+12, hand_r[1]+12)], fill=ink)

    elif pose == "confused":
        elbow_l = (head_x - int(80 * scale), shoulder_y + int(70 * scale))
        hand_l = (head_x - int(50 * scale), head_y + int(20 * scale))
        draw.line([(head_x - int(25 * scale), shoulder_y + int(15 * scale)), elbow_l], fill=ink, width=int(9 * scale))
        draw.line([elbow_l, hand_l], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_l[0]-12, hand_l[1]-12), (hand_l[0]+12, hand_l[1]+12)], fill=ink)

        elbow_r = (head_x + int(75 * scale), shoulder_y + int(90 * scale))
        hand_r = (head_x + int(20 * scale), pelvis_y - int(20 * scale))
        draw.line([(head_x + int(25 * scale), shoulder_y + int(15 * scale)), elbow_r], fill=ink, width=int(9 * scale))
        draw.line([elbow_r, hand_r], fill=ink, width=int(9 * scale))

    elif pose == "celebrating":
        # Both arms raised high in victory!
        hand_l = (head_x - int(120 * scale), shoulder_y - int(80 * scale))
        hand_r = (head_x + int(120 * scale), shoulder_y - int(80 * scale))
        draw.line([(head_x - int(25 * scale), shoulder_y + int(15 * scale)), hand_l], fill=ink, width=int(9 * scale))
        draw.line([(head_x + int(25 * scale), shoulder_y + int(15 * scale)), hand_r], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_l[0]-14, hand_l[1]-14), (hand_l[0]+14, hand_l[1]+14)], fill=ink)
        draw.ellipse([(hand_r[0]-14, hand_r[1]-14), (hand_r[0]+14, hand_r[1]+14)], fill=ink)

    else: # Default open explaining pose
        hand_l = (head_x - int(120 * scale), shoulder_y + int(60 * scale))
        hand_r = (head_x + int(120 * scale), shoulder_y + int(60 * scale))
        draw.line([(head_x - int(25 * scale), shoulder_y + int(15 * scale)), hand_l], fill=ink, width=int(9 * scale))
        draw.line([(head_x + int(25 * scale), shoulder_y + int(15 * scale)), hand_r], fill=ink, width=int(9 * scale))
        draw.ellipse([(hand_l[0]-12, hand_l[1]-12), (hand_l[0]+12, hand_l[1]+12)], fill=ink)
        draw.ellipse([(hand_r[0]-12, hand_r[1]-12), (hand_r[0]+12, hand_r[1]+12)], fill=ink)

    # HEAD (clean white fill, thick crisp black outline)
    head_bbox = [(head_x - head_r, head_y - head_r), (head_x + head_r, head_y + head_r)]
    draw.ellipse(head_bbox, fill=white, outline=ink, width=int(8 * scale))

    # FACE & EMOTION
    eye_offset_x = int(28 * scale)
    eye_y = head_y - int(10 * scale)
    eye_w = int(14 * scale)
    eye_h = int(22 * scale)

    # Eyes (two cute vertical ovals)
    draw.ellipse([(head_x - eye_offset_x - eye_w, eye_y - eye_h), (head_x - eye_offset_x + eye_w, eye_y + eye_h)], fill=ink)
    draw.ellipse([(head_x + eye_offset_x - eye_w, eye_y - eye_h), (head_x + eye_offset_x + eye_w, eye_y + eye_h)], fill=ink)
    # Specular reflections
    draw.ellipse([(head_x - eye_offset_x - 3, eye_y - eye_h + 3), (head_x - eye_offset_x + 5, eye_y - eye_h + 11)], fill=white)
    draw.ellipse([(head_x + eye_offset_x - 3, eye_y - eye_h + 3), (head_x + eye_offset_x + 5, eye_y - eye_h + 11)], fill=white)

    # Eyebrows
    brow_y = eye_y - int(34 * scale)
    if emotion == "surprised":
        # Raised arched eyebrows
        draw.arc([(head_x - eye_offset_x - int(24*scale), brow_y - int(12*scale)), 
                  (head_x - eye_offset_x + int(24*scale), brow_y + int(12*scale))], start=200, end=340, fill=ink, width=int(6 * scale))
        draw.arc([(head_x + eye_offset_x - int(24*scale), brow_y - int(12*scale)), 
                  (head_x + eye_offset_x + int(24*scale), brow_y + int(12*scale))], start=200, end=340, fill=ink, width=int(6 * scale))
        # Open mouth (surprised "O")
        mouth_y = head_y + int(42 * scale)
        draw.ellipse([(head_x - int(16*scale), mouth_y - int(22*scale)), (head_x + int(16*scale), mouth_y + int(22*scale))], fill=ink)
        draw.ellipse([(head_x - int(10*scale), mouth_y + int(6*scale)), (head_x + int(10*scale), mouth_y + int(20*scale))], fill=(244, 114, 182))
    elif emotion == "happy":
        draw.arc([(head_x - eye_offset_x - 18, brow_y), (head_x - eye_offset_x + 18, brow_y + 16)], start=190, end=350, fill=ink, width=int(5*scale))
        draw.arc([(head_x + eye_offset_x - 18, brow_y), (head_x + eye_offset_x + 18, brow_y + 16)], start=190, end=350, fill=ink, width=int(5*scale))
        mouth_y = head_y + int(36 * scale)
        draw.pieslice([(head_x - 28, mouth_y - 10), (head_x + 28, mouth_y + 36)], start=0, end=180, fill=ink)
    else: # Explaining / focused
        draw.line([(head_x - eye_offset_x - 18, brow_y), (head_x - eye_offset_x + 18, brow_y + 4)], fill=ink, width=int(5*scale))
        draw.line([(head_x + eye_offset_x - 18, brow_y + 4), (head_x + eye_offset_x + 18, brow_y)], fill=ink, width=int(5*scale))
        mouth_y = head_y + int(38 * scale)
        draw.arc([(head_x - 22, mouth_y - 12), (head_x + 22, mouth_y + 18)], start=20, end=160, fill=ink, width=int(6*scale))

# ==============================================================================
# FINANCIAL PROPS DRAWING FUNCTIONS
# ==============================================================================

def draw_inflation_arrow(draw, points, color=(220, 38, 38)):
    """Draws thick zigzag rising arrow with arrowhead."""
    # Draw segments
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=color, width=18)
    
    # Arrowhead at the last point
    p_last = points[-1]
    p_prev = points[-2]
    dx = p_last[0] - p_prev[0]
    dy = p_last[1] - p_prev[1]
    angle = math.atan2(dy, dx)
    
    arrow_len = 50
    arrow_w = 32
    tip = p_last
    left = (
        tip[0] - arrow_len * math.cos(angle) + arrow_w * math.sin(angle),
        tip[1] - arrow_len * math.sin(angle) - arrow_w * math.cos(angle)
    )
    right = (
        tip[0] - arrow_len * math.cos(angle) - arrow_w * math.sin(angle),
        tip[1] - arrow_len * math.sin(angle) + arrow_w * math.cos(angle)
    )
    draw.polygon([tip, left, right], fill=color)

def draw_price_tag(draw, x, y, tag_type="NEW", price="$5.00", angle_deg=0):
    """
    Renders hanging price tag (like in Stickonomics thumbnail: 'OLD $2.00', 'NEW $5.00')
    """
    w, h = 170, 240
    # Tag canvas
    tag_im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tag_im)
    
    # Tag polygon (luggage tag shape with top corners clipped)
    clip = 40
    pts = [
        (clip, 20), (w - clip, 20),
        (w - 10, clip + 20), (w - 10, h - 10),
        (10, h - 10), (10, clip + 20)
    ]
    tdraw.polygon(pts, fill=(255, 255, 255), outline=(20, 24, 33))
    # Reinforce outline
    for i in range(len(pts)):
        p1 = pts[i]
        p2 = pts[(i+1)%len(pts)]
        tdraw.line([p1, p2], fill=(20, 24, 33), width=6)
        
    # Tag hole at top
    tdraw.ellipse([(w//2 - 12, 36), (w//2 + 12, 60)], outline=(20, 24, 33), width=5)
    
    # Text
    if tag_type == "NEW":
        tdraw.text((w//2, 105), "NEW", fill=(20, 24, 33), font=get_font(32), anchor="mm")
        tdraw.text((w//2, 168), price, fill=(220, 38, 38), font=get_font(52), anchor="mm")
    else:
        tdraw.text((w//2, 105), "OLD", fill=(100, 116, 139), font=get_font(32), anchor="mm")
        tdraw.text((w//2, 168), price, fill=(71, 85, 105), font=get_font(46), anchor="mm")

    # Rotate
    if angle_deg != 0:
        tag_im = tag_im.rotate(angle_deg, resample=Image.BICUBIC, expand=True)

    # String loop
    draw.line([(x, y - 60), (x, y + 10)], fill=(71, 85, 105), width=3)
    return tag_im

def draw_coin_stack(draw, x, y, num_coins=6, scale=1.0):
    """Draws realistic 3D perspective gold coin stack."""
    gold_face = (250, 204, 21)
    gold_side = (217, 119, 6)
    ink = (20, 24, 33)
    
    cw = int(90 * scale)
    ch = int(28 * scale)
    step = int(16 * scale)
    
    # Ground shadow
    draw_shadow(draw, x, y + int(10 * scale), int(60 * scale), int(16 * scale))

    for i in range(num_coins):
        cy = y - (i * step)
        # Side cylinder rectangle
        draw.rectangle([(x - cw//2, cy - ch//2 + 10), (x + cw//2, cy + ch//2 + 10)], fill=gold_side, outline=ink, width=2)
        # Ribbed coin edge lines
        for r_x in range(x - cw//2 + 10, x + cw//2 - 5, 14):
            draw.line([(r_x, cy - ch//2 + 12), (r_x, cy + ch//2 + 8)], fill=(180, 83, 9), width=2)
        # Top face ellipse
        draw.ellipse([(x - cw//2, cy - ch//2), (x + cw//2, cy + ch//2)], fill=gold_face, outline=ink, width=3)
        # Inner coin rim & dollar symbol
        draw.ellipse([(x - cw//2 + 8, cy - ch//2 + 4), (x + cw//2 - 8, cy + ch//2 - 4)], outline=(245, 158, 11), width=2)
        if i == num_coins - 1:
            draw.text((x, cy), "$", fill=(180, 83, 9), font=get_font(int(22 * scale)), anchor="mm")

def draw_shopping_basket(draw, x, y, scale=1.0):
    """Draws red supermarket wire basket like in the thumbnail."""
    red = (185, 28, 28)
    ink = (20, 24, 33)
    
    # Shadow
    draw_shadow(draw, x, y + int(10 * scale), int(70 * scale), int(16 * scale))
    
    bw = int(130 * scale)
    bh = int(80 * scale)
    top_w = int(150 * scale)
    
    # Wire basket rim
    rim_pts = [
        (x - top_w//2, y - bh),
        (x + top_w//2, y - bh),
        (x + bw//2, y),
        (x - bw//2, y)
    ]
    draw.polygon(rim_pts, fill=(254, 226, 226), outline=red)
    draw.polygon(rim_pts, outline=ink)
    
    # Wire grid lines
    for i in range(1, 5):
        gx = x - top_w//2 + (top_w * i // 5)
        bgx = x - bw//2 + (bw * i // 5)
        draw.line([(gx, y - bh), (bgx, y)], fill=red, width=3)
    
    # Handle
    handle_pts = [
        (x - top_w//2 + 20, y - bh),
        (x - 20, y - bh - int(45 * scale)),
        (x + 20, y - bh - int(45 * scale)),
        (x + top_w//2 - 20, y - bh)
    ]
    for i in range(len(handle_pts)-1):
        draw.line([handle_pts[i], handle_pts[i+1]], fill=ink, width=6)

# ==============================================================================
# KINETIC KARAOKE CAPTIONS
# ==============================================================================

def draw_single_caption_line(draw, w, y, words, active_idx):
    font = get_font(52, bold=True)
    space_w = 18
    widths = []
    for wd in words:
        bbox = draw.textbbox((0, 0), wd.upper(), font=font)
        widths.append(bbox[2] - bbox[0])
    
    total_w = sum(widths) + space_w * (len(words) - 1)
    if total_w > w - 120:
        font = get_font(42, bold=True)
        widths = []
        for wd in words:
            bbox = draw.textbbox((0, 0), wd.upper(), font=font)
            widths.append(bbox[2] - bbox[0])
        total_w = sum(widths) + space_w * (len(words) - 1)
        
    start_x = (w - total_w) // 2
    cur_x = start_x
    for i, wd in enumerate(words):
        is_active = (i == active_idx)
        text_color = (255, 230, 0) if is_active else (255, 255, 255)
        draw.text(
            (cur_x, y),
            wd.upper(),
            font=font,
            fill=text_color,
            stroke_width=8,
            stroke_fill=(15, 23, 42)
        )
        cur_x += widths[i] + space_w

def draw_karaoke_captions(draw, w, y, words_list, active_word_idx):
    """
    Draws bold uppercase karaoke subtitles with radiant yellow active word highlight.
    White text, thick black outline, active word in #FFE600.
    Automatically wraps into 2 centered lines if long so text never overflows.
    """
    if len(words_list) > 5:
        mid = len(words_list) // 2
        line1_words = words_list[:mid]
        line2_words = words_list[mid:]
        
        a_idx_1 = active_word_idx if active_word_idx < mid else -1
        draw_single_caption_line(draw, w, y - 40, line1_words, a_idx_1)
        
        a_idx_2 = (active_word_idx - mid) if active_word_idx >= mid else -1
        draw_single_caption_line(draw, w, y + 40, line2_words, a_idx_2)
    else:
        draw_single_caption_line(draw, w, y, words_list, active_word_idx)

# ==============================================================================
# TEST FRAME RENDER (PROOF OF MATCHING STYLE)
# ==============================================================================

def render_stickonomics_sample_frame(out_path):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Top brand watermark
    draw.text((w // 2, 80), "WHERE MY DOLLAR GO", fill=(100, 116, 139), font=get_font(28), anchor="mm")
    draw.text((w // 2, 120), "The Truth About Money in 40 Seconds", fill=(148, 163, 184), font=get_font(24), anchor="mm")

    # Character position
    char_x = 360
    char_y = 1380
    draw_stickman(draw, char_x, char_y, pose="pointing_right", emotion="surprised", scale=1.15)

    # Supermarket shopping basket near feet
    draw_shopping_basket(draw, char_x - 170, char_y - 20, scale=1.1)

    # Rising Red Inflation Arrow
    arrow_pts = [
        (480, 1020),
        (560, 890),
        (620, 940),
        (760, 680),
        (880, 560)
    ]
    draw_inflation_arrow(draw, arrow_pts, color=(220, 38, 38))

    # Price Tags: OLD $2.00 and NEW $5.00
    tag_old = draw_price_tag(draw, 530, 920, tag_type="OLD", price="$2.00", angle_deg=4)
    im.paste(tag_old, (450, 930), tag_old)

    tag_new = draw_price_tag(draw, 680, 800, tag_type="NEW", price="$5.00", angle_deg=-6)
    im.paste(tag_new, (620, 810), tag_new)

    # Coin Stacks on floor
    draw_coin_stack(draw, 640, 1380, num_coins=5, scale=1.1)
    draw_coin_stack(draw, 740, 1380, num_coins=8, scale=1.1)
    draw_coin_stack(draw, 840, 1380, num_coins=6, scale=1.1)

    # Captions at lower center: "INTEREST OVER TIME" (OVER highlighted in yellow)
    draw_karaoke_captions(draw, w, y=1620, words_list=["INTEREST", "OVER", "TIME"], active_word_idx=1)

    im.save(out_path, "PNG")
    print(f"Sample frame rendered to {out_path}")

# ==============================================================================
# FULL 5-SCENE STICKONOMICS EXPLAINER PRODUCTION
# ==============================================================================

def draw_top_hud(draw, w, title_tag):
    draw.text((w // 2, 70), "WHERE MY DOLLAR GO", fill=(100, 116, 139), font=get_font(28), anchor="mm")
    draw.text((w // 2, 115), title_tag, fill=(148, 163, 184), font=get_font(24), anchor="mm")
    draw.line([(80, 155), (w - 80, 155)], fill=(226, 232, 240), width=3)

def render_scene_1_barter(out_path, caption="Thousands of years ago, people traded goods directly.", yword="traded"):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "The Barter Problem (Before Money)")

    # Title Banner
    draw.rounded_rectangle([(180, 220), (900, 310)], radius=20, fill=(241, 245, 249), outline=(203, 213, 225), width=3)
    draw.text((w // 2, 265), "THE BARTER PROBLEM", fill=(30, 41, 59), font=get_font(36), anchor="mm")

    # Stickman 1 (Left - has apple, wants fish)
    draw_stickman(draw, 320, 1380, pose="open_explaining", emotion="confused", scale=1.05)
    # Draw Apple near left hand
    draw.ellipse([(170, 880), (250, 960)], fill=(220, 38, 38), outline=(20, 24, 33), width=4)
    draw.line([(210, 880), (210, 850)], fill=(71, 85, 105), width=5)
    draw.text((210, 985), "Apples", fill=(71, 85, 105), font=get_font(28), anchor="mm")

    # Stickman 2 (Right - has fish, doesn't want apples)
    draw_stickman(draw, 760, 1380, pose="confused", emotion="surprised", scale=1.05)
    # Draw Fish near right hand
    draw.ellipse([(830, 900), (940, 960)], fill=(56, 189, 248), outline=(20, 24, 33), width=4)
    draw.polygon([(930, 930), (970, 890), (970, 970)], fill=(56, 189, 248), outline=(20, 24, 33))
    draw.ellipse([(855, 915), (865, 925)], fill=(20, 24, 33)) # eye
    draw.text((900, 985), "Fish", fill=(71, 85, 105), font=get_font(28), anchor="mm")

    # Big Red Question Mark / Conflict in middle
    draw.line([(480, 850), (600, 970)], fill=(220, 38, 38), width=14)
    draw.line([(600, 850), (480, 970)], fill=(220, 38, 38), width=14)
    draw.text((w // 2, 760), "NO MATCH!", fill=(220, 38, 38), font=get_font(42), anchor="mm")

    words = caption.split()
    y_idx = next((i for i, wd in enumerate(words) if yword.lower() in wd.lower()), 0)
    draw_karaoke_captions(draw, w, y=1620, words_list=words, active_word_idx=y_idx)
    im.save(out_path, "PNG")

def render_scene_2_invention(out_path, caption="Money was invented as a universal middleman!", yword="money"):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "The Invention of Universal Exchange")

    # Title Banner
    draw.rounded_rectangle([(160, 220), (920, 310)], radius=20, fill=(236, 253, 245), outline=(16, 185, 129), width=3)
    draw.text((w // 2, 265), "THE BIRTH OF MONEY", fill=(5, 150, 105), font=get_font(36), anchor="mm")

    # Happy Stickman holding cash in center
    draw_stickman(draw, 540, 1380, pose="holding_money", emotion="happy", scale=1.15)

    # Giant Gold Coin above
    cw, ch = 180, 180
    cx, cy = 540, 560
    draw_shadow(draw, cx, cy + 120, 100, 25)
    draw.ellipse([(cx - cw//2, cy - ch//2), (cx + cw//2, cy + ch//2)], fill=(250, 204, 21), outline=(20, 24, 33), width=6)
    draw.ellipse([(cx - cw//2 + 16, cy - ch//2 + 16), (cx + cw//2 - 16, cy + ch//2 - 16)], outline=(217, 119, 6), width=4)
    draw.text((cx, cy), "$", fill=(180, 83, 9), font=get_font(96), anchor="mm")

    # Green Dollar Bill Left
    draw.rounded_rectangle([(160, 820), (380, 960)], radius=12, fill=(220, 252, 231), outline=(22, 101, 52), width=5)
    draw.text((270, 890), "$100", fill=(22, 101, 52), font=get_font(56), anchor="mm")

    # Green Dollar Bill Right
    draw.rounded_rectangle([(700, 820), (920, 960)], radius=12, fill=(220, 252, 231), outline=(22, 101, 52), width=5)
    draw.text((810, 890), "$100", fill=(22, 101, 52), font=get_font(56), anchor="mm")

    # Coin stacks below
    draw_coin_stack(draw, 270, 1380, num_coins=6, scale=1.1)
    draw_coin_stack(draw, 810, 1380, num_coins=6, scale=1.1)

    words = caption.split()
    y_idx = next((i for i, wd in enumerate(words) if yword.lower() in wd.lower()), 0)
    draw_karaoke_captions(draw, w, y=1620, words_list=words, active_word_idx=y_idx)
    im.save(out_path, "PNG")

def render_scene_3_trust(out_path, caption="Paper money only works because society agrees it has value.", yword="agrees"):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "Why Does Paper Have Value? (Fiat Currency)")

    # Bank Pediment Architecture in background
    bank_x = 540
    bank_y = 480
    # Pediment Triangle
    draw.polygon([(bank_x - 300, bank_y), (bank_x, bank_y - 140), (bank_x + 300, bank_y)], fill=(241, 245, 249), outline=(20, 24, 33), width=5)
    draw.text((bank_x, bank_y - 45), "CENTRAL BANK", fill=(20, 24, 33), font=get_font(30), anchor="mm")
    # Columns
    for col_x in [bank_x - 240, bank_x - 80, bank_x + 80, bank_x + 240]:
        draw.rectangle([(col_x - 22, bank_y), (col_x + 22, bank_y + 240)], fill=(248, 250, 252), outline=(20, 24, 33), width=4)
    # Base
    draw.rectangle([(bank_x - 320, bank_y + 240), (bank_x + 320, bank_y + 280)], fill=(226, 232, 240), outline=(20, 24, 33), width=4)

    # Stickman examining paper money with magnifying glass
    draw_stickman(draw, 420, 1380, pose="pointing_right", emotion="surprised", scale=1.1)

    # Giant Dollar Bill with Trust Stamp
    bill_x, bill_y = 740, 1020
    draw.rounded_rectangle([(bill_x - 170, bill_y - 110), (bill_x + 170, bill_y + 110)], radius=16, fill=(240, 253, 244), outline=(22, 101, 52), width=5)
    draw.text((bill_x, bill_y - 30), "FEDERAL NOTE", fill=(21, 128, 61), font=get_font(26), anchor="mm")
    draw.text((bill_x, bill_y + 35), "$100", fill=(22, 101, 52), font=get_font(68), anchor="mm")
    # Red Trust Stamp Circle
    draw.ellipse([(bill_x - 90, bill_y - 80), (bill_x + 90, bill_y + 80)], outline=(220, 38, 38), width=5)
    draw.text((bill_x, bill_y), "TRUST", fill=(220, 38, 38), font=get_font(34), anchor="mm")

    words = caption.split()
    y_idx = next((i for i, wd in enumerate(words) if yword.lower() in wd.lower()), 0)
    draw_karaoke_captions(draw, w, y=1620, words_list=words, active_word_idx=y_idx)
    im.save(out_path, "PNG")

def render_scene_4_inflation(out_path, caption="Over time, rising inflation makes your dollars buy less.", yword="inflation"):
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    draw_top_hud(draw, w, "The Inflation Monster: Rising Prices")

    # Character position
    char_x = 360
    char_y = 1380
    draw_stickman(draw, char_x, char_y, pose="pointing_right", emotion="surprised", scale=1.15)

    # Supermarket shopping basket near feet
    draw_shopping_basket(draw, char_x - 170, char_y - 20, scale=1.1)

    # Rising Red Inflation Arrow
    arrow_pts = [
        (480, 1020),
        (560, 890),
        (620, 940),
        (760, 680),
        (880, 560)
    ]
    draw_inflation_arrow(draw, arrow_pts, color=(220, 38, 38))

    # Price Tags: OLD $2.00 and NEW $5.00
    tag_old = draw_price_tag(draw, 530, 920, tag_type="OLD", price="$2.00", angle_deg=4)
    im.paste(tag_old, (450, 930), tag_old)

    tag_new = draw_price_tag(draw, 680, 800, tag_type="NEW", price="$5.00", angle_deg=-6)
    im.paste(tag_new, (620, 810), tag_new)

    # Coin Stacks on floor
    draw_coin_stack(draw, 640, 1380, num_coins=5, scale=1.1)
    draw_coin_stack(draw, 740, 1380, num_coins=8, scale=1.1)
    draw_coin_stack(draw, 840, 1380, num_coins=6, scale=1.1)

    words = caption.split()
    y_idx = next((i for i, wd in enumerate(words) if yword.lower() in wd.lower()), 0)
    draw_karaoke_captions(draw, w, y=1620, words_list=words, active_word_idx=y_idx)
    im.save(out_path, "PNG")

def render_generic_stickman_scene(scene_spec, out_path, caption, yword, scene_idx, total_scenes):
    """
    Renders any scene specification from topics.json into the Stickonomics visual style:
    - Pure white clean canvas (1080x1920)
    - Top branding header & progress indicator
    - Expressive stickman with appropriate pose and facial emotion
    - Illustrated card with key details and metric badge
    - Financial props (coin stacks, dollar notes, arrows)
    - Kinetic karaoke caption with radiant yellow word highlight
    """
    w, h = 1080, 1920
    im = Image.new("RGB", (w, h), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)

    # Top brand bar
    draw_top_hud(draw, w, scene_spec.get("subtitle", "Financial Literacy Explainer"))

    # Scene Title Card
    title_text = scene_spec.get("title", "")
    draw.rounded_rectangle([(120, 200), (960, 310)], radius=24, fill=(248, 250, 252), outline=(203, 213, 225), width=3)
    draw.text((w // 2, 255), title_text.upper(), fill=(15, 23, 42), font=get_font(36, bold=True), anchor="mm")

    # Pick character emotion and pose based on scene index / content
    if scene_idx == 0:
        pose = "pointing_right"
        emotion = "surprised"
    elif scene_idx == total_scenes - 1:
        pose = "celebrating"
        emotion = "happy"
    elif "problem" in title_text.lower() or "cost" in title_text.lower() or "inflation" in title_text.lower():
        pose = "confused"
        emotion = "surprised"
    elif "trade" in title_text.lower() or "market" in title_text.lower() or "money" in title_text.lower():
        pose = "holding_money"
        emotion = "happy"
    else:
        pose = "open_explaining"
        emotion = "explaining"

    # Draw stickman character on left side
    char_x = 320
    char_y = 1380
    draw_stickman(draw, char_x, char_y, pose=pose, emotion=emotion, scale=1.05)

    # Draw Detail Box on right side
    box_left = 490
    box_top = 400
    box_right = 1000
    box_bottom = 1200
    draw.rounded_rectangle([(box_left, box_top), (box_right, box_bottom)], radius=24, fill=(241, 245, 249), outline=(203, 213, 225), width=3)

    # Metric Header inside card
    metric_lbl = scene_spec.get("metric_label", "KEY TAKEAWAY").upper()
    metric_v = scene_spec.get("metric_val", "100%").upper()
    draw.rounded_rectangle([(box_left + 30, box_top + 30), (box_right - 30, box_top + 150)], radius=16, fill=(255, 255, 255), outline=(16, 185, 129), width=3)
    draw.text((box_left + 50, box_top + 50), metric_lbl, fill=(100, 116, 139), font=get_font(22, bold=True))
    draw.text((box_left + 50, box_top + 90), metric_v, fill=(5, 150, 105), font=get_font(34, bold=True))

    # Detail bullet lines
    details = scene_spec.get("details", [])
    cur_y = box_top + 190
    for det in details:
        # Wrap detail text
        words = det.split()
        lines = []
        cur_l = []
        for wd in words:
            if len(" ".join(cur_l + [wd])) > 24:
                lines.append(" ".join(cur_l))
                cur_l = [wd]
            else:
                cur_l.append(wd)
        if cur_l:
            lines.append(" ".join(cur_l))

        # Clean Emerald Bullet Dot
        draw.ellipse([(box_left + 32, cur_y + 6), (box_left + 46, cur_y + 20)], fill=(16, 185, 129))
        for line_str in lines:
            draw.text((box_left + 65, cur_y), line_str, fill=(30, 41, 59), font=get_font(26, bold=False))
            cur_y += 38
        cur_y += 18

    # Props below stickman
    if scene_idx == total_scenes - 1:
        # Final celebratory scene: rising green arrow & big coin stack
        draw_coin_stack(draw, 320, 1420, num_coins=9, scale=1.1)
        draw_coin_stack(draw, 420, 1420, num_coins=14, scale=1.1)
    else:
        # Floor coin stacks
        draw_coin_stack(draw, char_x - 120, char_y + 10, num_coins=4, scale=0.95)
        draw_coin_stack(draw, char_x + 120, char_y + 10, num_coins=6, scale=0.95)

    # Captions at bottom
    words = caption.split()
    y_idx = next((i for i, wd in enumerate(words) if yword.lower() in wd.lower()), 0)
    draw_karaoke_captions(draw, w, y=1620, words_list=words, active_word_idx=y_idx)

    im.save(out_path, "PNG")

def render_stickman_video(topic, output_mp4):
    """
    Renders an end-to-end Stickonomics video for any topic object:
    - Generates human speech (en-US-AndrewNeural)
    - Masters audio with ducked background music
    - Renders all scene cards with stickman & props
    - Encodes 1080x1920 MP4 at 30fps
    """
    work_dir = OUTPUT_DIR / topic["id"]
    work_dir.mkdir(parents=True, exist_ok=True)
    raw_voice = work_dir / "voice_raw.mp3"
    mastered_audio = work_dir / "audio_mastered.wav"

    script = topic.get("script", topic.get("hook", ""))
    scenes = topic.get("scenes", [])

    print(f"--- Synthesizing Stickonomics Voice for {topic['id']} ---")
    asyncio.run(synthesize_voice(script, voice="en-US-AndrewNeural", out_path=raw_voice))
    duration = get_audio_duration(raw_voice)
    master_audio(raw_voice, mastered_audio)

    scene_dur = duration / max(1, len(scenes))
    concat_lines = []

    for i, spec in enumerate(scenes):
        img_path = work_dir / f"scene_{i}.png"
        details = spec.get("details", [""])
        caption_line = details[0] if details else spec.get("title", "")
        # Highlight first key word
        first_word = caption_line.split()[0] if caption_line.split() else "dollar"
        
        # Use specialized scene if it's the custom how_money_works, else use generic stickman scene
        if topic.get("id") == "explainer_000_how_money_works_stickman":
            special_scenes = [render_scene_1_barter, render_scene_2_invention, render_scene_3_trust, render_scene_4_inflation, render_scene_5_investing]
            special_scenes[min(i, len(special_scenes)-1)](img_path, caption_line, first_word)
        else:
            render_generic_stickman_scene(spec, img_path, caption_line, first_word, i, len(scenes))

        concat_lines.append(f"file '{img_path.resolve().as_posix()}'")
        concat_lines.append(f"duration {scene_dur:.3f}")

    # Append last frame for concat demuxer
    concat_lines.append(f"file '{(work_dir / f'scene_{len(scenes)-1}.png').resolve().as_posix()}'")
    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print(f"Encoding final MP4 to {output_mp4}...")
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
    print(f"[SUCCESS] Stickman Explainer Video Built: {output_mp4}")
    return output_mp4

# ==============================================================================
# AUDIO & MASTERING
# ==============================================================================

async def synthesize_voice(text, voice="en-US-AndrewNeural", out_path="voice.mp3"):
    import edge_tts
    comm = edge_tts.Communicate(text, voice, rate="+2%", pitch="-1Hz")
    await comm.save(str(out_path))

def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def master_audio(voice_path, output_audio_path):
    filter_complex = (
        "[0:a]highpass=f=70,equalizer=f=120:t=q:w=1:g=3,equalizer=f=3200:t=q:w=1:g=2,volume=1.3[v];"
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

# ==============================================================================
# MAIN FULL SHORT BUILDER
# ==============================================================================

def produce_stickman_explainer_video():
    work_dir = OUTPUT_DIR / "how_money_works_stickman"
    work_dir.mkdir(parents=True, exist_ok=True)
    raw_voice = work_dir / "voice_raw.mp3"
    mastered_audio = work_dir / "audio_mastered.wav"
    output_mp4 = ROOT / "renders" / "explainer_how_money_works_stickman.mp4"

    script = (
        "Thousands of years ago, if you wanted fish, you had to trade apples. "
        "Money was invented as the universal middleman so everyone could trade easily! "
        "A dollar bill is just paper, but it works because all of society agrees on its value. "
        "Over time, inflation makes prices rise, meaning your dollars buy less. "
        "To beat inflation, don't just hold cash, invest it! "
        "Subscribe to WhereMyDollarGo for every dollar explained!"
    )

    print("==================================================================")
    print("  Building Stickonomics-Style Animated Explainer: How Money Works ")
    print("==================================================================")

    print("\n1. Synthesizing energetic conversational voiceover (en-US-AndrewNeural)...")
    asyncio.run(synthesize_voice(script, voice="en-US-AndrewNeural", out_path=raw_voice))
    duration = get_audio_duration(raw_voice)
    print(f"Audio duration: {duration:.2f} seconds")

    print("\n2. Applying broadcast EQ & ducked background music...")
    master_audio(raw_voice, mastered_audio)

    print("\n3. Rendering Stickonomics illustrated visual scenes...")
    scenes = [
        (render_scene_1_barter, "Years ago, you had to trade apples for fish.", "trade"),
        (render_scene_2_invention, "Money was invented as the universal middleman!", "Money"),
        (render_scene_3_trust, "Paper money works because society agrees on its value.", "agrees"),
        (render_scene_4_inflation, "Inflation makes prices rise, so your dollars buy less.", "Inflation"),
        (render_scene_5_investing, "Beat inflation by investing your dollars wisely!", "investing")
    ]

    scene_dur = duration / len(scenes)
    concat_lines = []
    for i, (renderer, caption, yword) in enumerate(scenes):
        img_path = work_dir / f"scene_{i}.png"
        renderer(img_path, caption, yword)
        concat_lines.append(f"file '{img_path.resolve().as_posix()}'")
        concat_lines.append(f"duration {scene_dur:.3f}")

    concat_lines.append(f"file '{(work_dir / f'scene_{len(scenes)-1}.png').resolve().as_posix()}'")
    concat_file = work_dir / "concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        f.write("\n".join(concat_lines))

    print("\n4. Encoding 1080x1920 MP4 video with FFmpeg...")
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
    print(f"\n[SUCCESS] Stickonomics Explainer Rendered: {output_mp4} ({os.path.getsize(output_mp4):,} bytes)")

    return output_mp4, script

if __name__ == "__main__":
    mp4, script = produce_stickman_explainer_video()
    print("Render complete:", mp4)
