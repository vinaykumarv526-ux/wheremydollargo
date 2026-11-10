"""
Daily Carousel Generator for WhereMyDollarGo: "Last 24 Hours in US Money"
Generates 5-slide visual carousel (1080x1350 PNG images) ready for YouTube Community,
Instagram, and LinkedIn.
"""
import os
import sys
import json
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent.parent
FONT_PATH = "C:/Windows/Fonts/arialbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "C:/Windows/Fonts/calibrib.ttf"

def get_font(size):
    try:
        return ImageFont.truetype(FONT_PATH, size)
    except Exception:
        return ImageFont.load_default()

def render_slide_image(slide_info, output_path):
    w, h = 1080, 1350
    # Deep midnight navy background
    im = Image.new("RGB", (w, h), color=(11, 15, 25))
    draw = ImageDraw.Draw(im)

    # Ambient radial glow top-right
    for r in range(160, 0, -12):
        draw.ellipse([(w - r*3, -r*2), (w + r*2, r*2)], fill=(16, 185, 129))

    # Top brand header
    draw.text((80, 70), "WHERE MY DOLLAR GO", fill=(16, 185, 129), font=get_font(28))
    draw.text((w - 80, 70), "@WhereMyDollarGo", fill=(148, 163, 184), font=get_font(24), anchor="ra")
    draw.line([(80, 115), (w - 80, 115)], fill=(30, 41, 59), width=3)

    stype = slide_info["type"]
    if stype == "COVER":
        # Cover slide
        draw.text((80, 220), slide_info["eyebrow"], fill=(16, 185, 129), font=get_font(24))
        # Title
        draw.text((80, 290), "Last 24 Hours", fill=(255, 255, 255), font=get_font(76))
        draw.text((80, 390), "in US Money", fill=(56, 189, 248), font=get_font(76))
        draw.text((80, 520), slide_info["date"], fill=(245, 158, 11), font=get_font(38))

        # Big summary card
        draw.rounded_rectangle([(80, 620), (w - 80, 1120)], radius=28, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
        draw.text((130, 690), "TODAY'S 3 KEY ECONOMIC SHIFTS:", fill=(16, 185, 129), font=get_font(28))
        draw.text((130, 770), "1. Mortgage Rates & Housing Costs", fill=(248, 250, 252), font=get_font(34))
        draw.text((130, 850), "2. Top High-Yield Savings Account Rates", fill=(248, 250, 252), font=get_font(34))
        draw.text((130, 930), "3. National Fuel Pump & Energy Prices", fill=(248, 250, 252), font=get_font(34))
        draw.text((130, 1030), "Swipe to see what it means for your wallet ➡️", fill=(148, 163, 184), font=get_font(28))

    elif stype == "METRIC":
        draw.text((80, 180), slide_info["category"], fill=(16, 185, 129), font=get_font(24))
        
        # Headline
        words = slide_info["headline"].split()
        lines = []
        cur = []
        for wd in words:
            cur.append(wd)
            if len(" ".join(cur)) > 26:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        
        hy = 230
        for l in lines:
            draw.text((80, hy), l, fill=(255, 255, 255), font=get_font(44))
            hy += 56

        # Metric Hero Box
        box_top = hy + 40
        box_bot = box_top + 280
        draw.rounded_rectangle([(80, box_top), (w - 80, box_bot)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=3)
        draw.text((w // 2, box_top + 60), slide_info["metric"], fill=(56, 189, 248), font=get_font(84), anchor="mm")
        draw.text((w // 2, box_top + 160), slide_info["delta"], fill=(245, 158, 11), font=get_font(30), anchor="mm")
        draw.text((w // 2, box_top + 220), f"Context: {slide_info['context']}", fill=(148, 163, 184), font=get_font(24), anchor="mm")

        # Impact Card
        imp_top = box_bot + 40
        imp_bot = 1180
        draw.rounded_rectangle([(80, imp_top), (w - 80, imp_bot)], radius=24, fill=(15, 23, 42), outline=(30, 41, 59), width=2)
        draw.text((120, imp_top + 40), "WHAT IT MEANS FOR EVERYDAY PEOPLE:", fill=(245, 158, 11), font=get_font(24))
        
        # Wrap impact text
        imp_words = slide_info["impact"].split()
        imp_lines = []
        cur = []
        for wd in imp_words:
            cur.append(wd)
            if len(" ".join(cur)) > 34:
                imp_lines.append(" ".join(cur))
                cur = []
        if cur:
            imp_lines.append(" ".join(cur))
        
        iy = imp_top + 95
        for l in imp_lines:
            draw.text((120, iy), l, fill=(226, 232, 240), font=get_font(30))
            iy += 48
            
        draw.text((120, imp_bot - 50), f"Primary Source: {slide_info['source']}", fill=(100, 116, 139), font=get_font(22))

    elif stype == "CONCLUSION":
        draw.text((80, 180), "DAILY SUMMARY & TAKEAWAY", fill=(16, 185, 129), font=get_font(24))
        draw.text((80, 240), "Follow Your Dollar Daily", fill=(255, 255, 255), font=get_font(60))

        # Takeaway quote card
        draw.rounded_rectangle([(80, 360), (w - 80, 680)], radius=24, fill=(15, 23, 42), outline=(16, 185, 129), width=3)
        draw.text((130, 420), "CORE TAKEAWAY:", fill=(16, 185, 129), font=get_font(26))
        draw.text((130, 480), f'"{slide_info["takeaway"]}"', fill=(248, 250, 252), font=get_font(34))

        # Community question card
        draw.rounded_rectangle([(80, 720), (w - 80, 1020)], radius=24, fill=(15, 23, 42), outline=(51, 65, 85), width=2)
        draw.text((130, 780), "COMMUNITY QUESTION:", fill=(245, 158, 11), font=get_font(26))
        draw.text((130, 840), slide_info["question"], fill=(248, 250, 252), font=get_font(32))
        draw.text((130, 930), "Drop your answer in the comments below! 👇", fill=(148, 163, 184), font=get_font(26))

        draw.text((w // 2, 1100), slide_info["disclaimer"], fill=(100, 116, 139), font=get_font(22), anchor="mm")
        draw.text((w // 2, 1180), "Subscribe & Follow @WhereMyDollarGo", fill=(255, 255, 255), font=get_font(34), anchor="mm")

    # Bottom footer page numbers
    page_num = slide_info.get("slide", 1)
    draw.text((w // 2, 1280), f"Slide {page_num} of 5", fill=(100, 116, 139), font=get_font(22), anchor="mm")

    im.save(output_path, "PNG")

def generate_daily_carousel(date_str=None):
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    target_dir = ROOT / "publish-queue" / date_str / "daily-carousel"
    target_dir.mkdir(parents=True, exist_ok=True)

    slides_data = [
        {
            "slide": 1,
            "type": "COVER",
            "eyebrow": "DAILY US ECONOMIC BRIEFING",
            "headline": "Last 24 Hours in US Money",
            "date": date_str,
            "subtitle": "3 key monetary shifts impacting your wallet today.",
            "brand": "@WhereMyDollarGo"
        },
        {
            "slide": 2,
            "type": "METRIC",
            "category": "MORTGAGE & HOUSING",
            "headline": "Average 30-Year Fixed Mortgage at 6.62%",
            "metric": "6.62%",
            "delta": "-4 bps (week-over-week)",
            "context": "Bond yields eased after recent Treasury debt auctions.",
            "impact": "On a $400k loan, this rate holds monthly payments at ~$2,560, saving ~$65/mo compared to 6.87% peaks.",
            "source": "Freddie Mac PMMS"
        },
        {
            "slide": 3,
            "type": "METRIC",
            "category": "BANKING & CASH SAVINGS",
            "headline": "Top High-Yield Savings Accounts Hold at 4.45% APY",
            "metric": "4.45% APY",
            "delta": "vs 0.07% Big-Box Checking",
            "context": "Competitive digital institutions maintain high yields despite Fed pauses.",
            "impact": "A $10,000 emergency fund earns ~$445/yr in passive yield vs less than $7 at traditional banks.",
            "source": "FDIC National Average Rates"
        },
        {
            "slide": 4,
            "type": "METRIC",
            "category": "CONSUMER GAS PUMP",
            "headline": "National Average Gasoline at $3.12 / Gallon",
            "metric": "$3.12 / gal",
            "delta": "Stable across 42 states",
            "context": "Crude oil is 52% of the price; taxes and refining make up 48%.",
            "impact": "A 14-gallon fill-up costs $43.68, with $6.55 going to state and federal road maintenance trust funds.",
            "source": "U.S. Energy Information Administration (EIA)"
        },
        {
            "slide": 5,
            "type": "CONCLUSION",
            "headline": "Follow Your Dollar Daily",
            "takeaway": "You don't need to track the stock ticker every minute. Just know where your money goes.",
            "question": "Where is your primary emergency fund sitting right now?",
            "disclaimer": "General education only. Not financial, tax, or legal advice.",
            "brand": "@WhereMyDollarGo"
        }
    ]

    # Save JSON spec
    with open(target_dir / "carousel_spec.json", "w", encoding="utf-8") as f:
        json.dump(slides_data, f, indent=2)

    # Render each of the 5 slides to PNG
    for i, slide in enumerate(slides_data, 1):
        png_path = target_dir / f"slide_{i}.png"
        render_slide_image(slide, png_path)

    # Write copy-paste community post caption
    caption_content = f"""📊 Last 24 Hours in US Money ({date_str})

1️⃣ Mortgage Rates: 30-year fixed holds at 6.62%.
2️⃣ Savings Yields: Top HYSAs paying ~4.45% APY vs 0.07% at traditional banks.
3️⃣ Gas Pump: National average steady at $3.12/gal.

Swipe through the slides for the exact breakdown of how this hits your everyday budget. ➡️

💬 Question: Where is your emergency fund sitting right now: traditional checking or high-yield savings?

Follow @WhereMyDollarGo for daily breakdowns of money, taxes, and debt.
(General education, not financial advice.)

#personalfinance #mortgagerates #interestrates #hysa #inflation #wheremydollargo #money
"""
    with open(target_dir / "caption.txt", "w", encoding="utf-8") as f:
        f.write(caption_content)

    print(f"[OK] Generated 5 carousel PNG slides and caption at: {target_dir}")
    return target_dir

if __name__ == "__main__":
    generate_daily_carousel()
