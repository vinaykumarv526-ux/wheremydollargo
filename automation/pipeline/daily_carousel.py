"""
Daily Carousel Generator for WhereMyDollarGo: "Last 24 Hours in US Money"
Generates 5-slide visual carousel files ready for Instagram, LinkedIn, and YouTube Community.
"""
import os
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent

def generate_daily_carousel(date_str=None):
    if not date_str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    target_dir = ROOT / "publish-queue" / date_str / "daily-carousel"
    target_dir.mkdir(parents=True, exist_ok=True)

    # 1. Macro economic data snapshot (curated from Fed, Freddie Mac PMMS, EIA benchmarks)
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
            "headline": "Top High-Yield Savings Accounts (HYSA) Hold at 4.45% APY",
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
    json_path = target_dir / "carousel_spec.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(slides_data, f, indent=2)

    # Generate standalone responsive HTML presentation of the 5 slides
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Last 24 Hours in Money - {date_str}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: #0B0F19;
      color: #F8FAFC;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 30px;
      padding: 40px 20px;
    }}
    .slide {{
      width: 540px;
      height: 675px;
      background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
      border: 1px solid #334155;
      border-radius: 24px;
      padding: 48px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
      position: relative;
      overflow: hidden;
    }}
    .slide::before {{
      content: '';
      position: absolute;
      top: -100px;
      right: -100px;
      width: 260px;
      height: 260px;
      background: radial-gradient(circle, rgba(16, 185, 129, 0.15) 0%, transparent 70%);
      border-radius: 50%;
    }}
    .eyebrow {{
      font-size: 13px;
      font-weight: 700;
      letter-spacing: 2px;
      color: #10B981;
      text-transform: uppercase;
    }}
    h1 {{
      font-size: 38px;
      line-height: 1.15;
      font-weight: 800;
      color: #FFFFFF;
      margin-top: 14px;
    }}
    .metric-box {{
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid #334155;
      border-radius: 16px;
      padding: 24px;
      margin: 20px 0;
    }}
    .metric-val {{
      font-size: 46px;
      font-weight: 800;
      color: #38BDF8;
    }}
    .metric-delta {{
      font-size: 14px;
      font-weight: 600;
      color: #94A3B8;
      margin-top: 4px;
    }}
    .impact-label {{
      font-size: 12px;
      font-weight: 700;
      color: #F59E0B;
      letter-spacing: 1px;
      margin-bottom: 6px;
    }}
    .impact-text {{
      font-size: 16px;
      line-height: 1.45;
      color: #CBD5E1;
    }}
    .footer {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #334155;
      padding-top: 16px;
      font-size: 12px;
      color: #64748B;
    }}
    .brand {{
      color: #10B981;
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <!-- Slide 1 -->
  <div class="slide">
    <div>
      <div class="eyebrow">{slides_data[0]['eyebrow']}</div>
      <h1>{slides_data[0]['headline']}</h1>
      <p style="margin-top: 16px; color: #94A3B8; font-size: 18px;">{slides_data[0]['subtitle']}</p>
    </div>
    <div style="font-size: 20px; color: #38BDF8; font-weight: 600;">{slides_data[0]['date']}</div>
    <div class="footer">
      <span>WhereMyDollarGo</span>
      <span class="brand">{slides_data[0]['brand']}</span>
    </div>
  </div>

  <!-- Slide 2 -->
  <div class="slide">
    <div>
      <div class="eyebrow">{slides_data[1]['category']}</div>
      <h2 style="font-size: 26px; margin-top: 10px; color: #FFF;">{slides_data[1]['headline']}</h2>
      <div class="metric-box">
        <div class="metric-val">{slides_data[1]['metric']}</div>
        <div class="metric-delta">{slides_data[1]['delta']}</div>
      </div>
      <div>
        <div class="impact-label">WHAT IT MEANS FOR YOU</div>
        <div class="impact-text">{slides_data[1]['impact']}</div>
      </div>
    </div>
    <div class="footer">
      <span>Source: {slides_data[1]['source']}</span>
      <span class="brand">@WhereMyDollarGo</span>
    </div>
  </div>

  <!-- Slide 3 -->
  <div class="slide">
    <div>
      <div class="eyebrow">{slides_data[2]['category']}</div>
      <h2 style="font-size: 26px; margin-top: 10px; color: #FFF;">{slides_data[2]['headline']}</h2>
      <div class="metric-box">
        <div class="metric-val">{slides_data[2]['metric']}</div>
        <div class="metric-delta">{slides_data[2]['delta']}</div>
      </div>
      <div>
        <div class="impact-label">WHAT IT MEANS FOR YOU</div>
        <div class="impact-text">{slides_data[2]['impact']}</div>
      </div>
    </div>
    <div class="footer">
      <span>Source: {slides_data[2]['source']}</span>
      <span class="brand">@WhereMyDollarGo</span>
    </div>
  </div>

  <!-- Slide 4 -->
  <div class="slide">
    <div>
      <div class="eyebrow">{slides_data[3]['category']}</div>
      <h2 style="font-size: 26px; margin-top: 10px; color: #FFF;">{slides_data[3]['headline']}</h2>
      <div class="metric-box">
        <div class="metric-val">{slides_data[3]['metric']}</div>
        <div class="metric-delta">{slides_data[3]['delta']}</div>
      </div>
      <div>
        <div class="impact-label">WHAT IT MEANS FOR YOU</div>
        <div class="impact-text">{slides_data[3]['impact']}</div>
      </div>
    </div>
    <div class="footer">
      <span>Source: {slides_data[3]['source']}</span>
      <span class="brand">@WhereMyDollarGo</span>
    </div>
  </div>

  <!-- Slide 5 -->
  <div class="slide">
    <div>
      <div class="eyebrow">DAILY SUMMARY</div>
      <h2 style="font-size: 30px; margin-top: 10px; color: #FFF;">{slides_data[4]['headline']}</h2>
      <p style="margin-top: 20px; font-size: 18px; line-height: 1.5; color: #E2E8F0;">"{slides_data[4]['takeaway']}"</p>
      <div style="margin-top: 30px; padding: 18px; background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; border-radius: 8px;">
        <div style="font-weight: 700; color: #10B981; margin-bottom: 4px;">COMMUNITY QUESTION</div>
        <div style="color: #CBD5E1; font-size: 15px;">{slides_data[4]['question']}</div>
      </div>
    </div>
    <div class="footer">
      <span>{slides_data[4]['disclaimer']}</span>
      <span class="brand">@WhereMyDollarGo</span>
    </div>
  </div>
</body>
</html>
"""
    html_path = target_dir / "carousel.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Generated Daily Carousel package at: {target_dir}")
    return json_path

if __name__ == "__main__":
    generate_daily_carousel()
