"""
Batch Video Producer & Scheduler for WhereMyDollarGo
Generates the first batch of 3 high-impact finance Shorts:
- Video 1: Published NOW
- Video 2: Scheduled for Today's Midday Peak (12:30 PM ET)
- Video 3: Scheduled for Today's Prime Evening Peak (6:30 PM ET)
"""
import os
import sys
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from video_engine import render_short_video
from pipeline.uploader import upload_to_youtube

ROOT = Path(__file__).resolve().parent.parent

def run_batch():
    now_utc = datetime.now(timezone.utc)
    today_date = now_utc.strftime("%Y-%m-%d")

    # Target publish times
    # 1. Now (Immediate)
    # 2. Today 12:30 PM ET = 17:30 UTC
    # 3. Today 6:30 PM ET  = 23:30 UTC
    dt_midday = datetime(now_utc.year, now_utc.month, now_utc.day, 17, 30, tzinfo=timezone.utc)
    dt_evening = datetime(now_utc.year, now_utc.month, now_utc.day, 23, 30, tzinfo=timezone.utc)

    # If midday has already passed in UTC, push to tomorrow
    if dt_midday < now_utc + timedelta(minutes=15):
        dt_midday += timedelta(days=1)
    if dt_evening < now_utc + timedelta(minutes=15):
        dt_evening += timedelta(days=1)

    batch = [
        {
            "id": "short_001_paycheck",
            "title": "Where Does $100 of Your Paycheck Actually Go?",
            "script": (
                "You just earned one hundred dollars on paper. But before that direct deposit hits your checking account, "
                "where did twenty-four dollars instantly disappear? "
                "First comes mandatory FICA: six dollars and twenty cents goes to Social Security, and one dollar forty-five cents to Medicare. "
                "Next is federal income tax. For a typical median US earner, that takes about ten dollars and fifty cents. "
                "Then, most states take another four dollars and fifty cents. "
                "Add it up, and out of your one hundred dollars, you keep roughly seventy-seven dollars and thirty-five cents. "
                "Follow the trail so you always know where your dollar went. Subscribe to WhereMyDollarGo!"
            ),
            "scenes": [
                {
                    "title": "Where Does $100 of Your Paycheck Go?",
                    "subtitle": "Gross Pay vs Take-Home Net",
                    "metric_label": "Starting Gross Earnings",
                    "metric_val": "$100.00",
                    "details": [
                        "Gross salary earned on paper",
                        "Before payroll tax deductions"
                    ]
                },
                {
                    "title": "Deduction 1: Mandatory FICA",
                    "subtitle": "Social Security & Medicare Trust Funds",
                    "metric_label": "Total FICA Tax Cut",
                    "metric_val": "-$7.65",
                    "details": [
                        "$6.20 to Social Security (OASDI)",
                        "$1.45 to Medicare Hospital Insurance",
                        "Statutory mandatory federal payroll tax"
                    ]
                },
                {
                    "title": "Deduction 2: Federal Income Tax",
                    "subtitle": "US Treasury General Fund",
                    "metric_label": "Federal Income Tax (Effective)",
                    "metric_val": "-$10.50",
                    "details": [
                        "Median US earner effective rate (~10.5%)",
                        "Funds defense, infrastructure, and services",
                        "Progressive marginal brackets apply"
                    ]
                },
                {
                    "title": "Deduction 3: State Income Tax",
                    "subtitle": "State & Local Infrastructure",
                    "metric_label": "State Tax (National Average)",
                    "metric_val": "-$4.50",
                    "details": [
                        "Varies from 0% (TX, FL, WA) to 9%+",
                        "Weighted national average: ~$4.50 per $100",
                        "Funds state highways, schools, police"
                    ]
                },
                {
                    "title": "Your Final Take-Home Cash",
                    "subtitle": "What Actually Hits Your Direct Deposit",
                    "metric_label": "Actual Net Direct Deposit",
                    "metric_val": "$77.35",
                    "details": [
                        "You keep ~77.35% of gross earnings",
                        "Excludes voluntary 401(k) / health plans",
                        "Follow your money with @WhereMyDollarGo"
                    ]
                }
            ],
            "schedule_iso": None, # Publish NOW
            "tags": ["paycheck", "taxes", "fica", "wheremydollargo", "finance", "money"]
        },
        {
            "id": "short_002_gas_money",
            "title": "Where Does $100 of Gas Money Actually Go?",
            "script": (
                "You just pumped one hundred dollars of gasoline into your car. "
                "How much of that one hundred dollars did the gas station actually keep? "
                "Fifty-two dollars goes directly to crude oil extraction. "
                "Nineteen dollars pays for industrial refining. "
                "Fifteen dollars vanishes into state and federal fuel excise taxes. "
                "Fourteen dollars covers transportation and distribution. "
                "The gas station owner? They keep less than two dollars in net profit. "
                "They make their real money selling you snacks and coffee inside. "
                "Subscribe to WhereMyDollarGo for daily breakdowns!"
            ),
            "scenes": [
                {
                    "title": "Where Does $100 of Gas Money Go?",
                    "subtitle": "Pump Price Dissection",
                    "metric_label": "Total Spent at the Pump",
                    "metric_val": "$100.00",
                    "details": [
                        "Retail gasoline consumer expenditure",
                        "Source: US Energy Information Admin (EIA)"
                    ]
                },
                {
                    "title": "The Biggest Slice: Crude Oil",
                    "subtitle": "Drilling & Global Barrel Pricing",
                    "metric_label": "Crude Oil Cost",
                    "metric_val": "$52.00",
                    "details": [
                        "Over half of every dollar pays for crude",
                        "Driven by global OPEC+ supply and demand",
                        "Unrefined raw petroleum"
                    ]
                },
                {
                    "title": "Refining & Processing",
                    "subtitle": "Cracking Crude into Usable Fuel",
                    "metric_label": "Refining Margin & Cost",
                    "metric_val": "$19.00",
                    "details": [
                        "Refinery operations and crack spreads",
                        "Summer vs winter seasonal fuel blends",
                        "Environmental standard compliance"
                    ]
                },
                {
                    "title": "Government Excise Taxes",
                    "subtitle": "Highway Trust Funds",
                    "metric_label": "Federal & State Taxes",
                    "metric_val": "$15.00",
                    "details": [
                        "Federal tax: 18.4 cents per gallon",
                        "State average: ~32.5 cents per gallon",
                        "Dedicated to road and bridge repair"
                    ]
                },
                {
                    "title": "The Station's Real Profit",
                    "subtitle": "Why They Need You to Buy Snacks",
                    "metric_label": "Gas Station Net Margin",
                    "metric_val": "< $2.00",
                    "details": [
                        "Credit card swipe fees eat 2.5% to 3%",
                        "Gas stations make profits on coffee & snacks",
                        "Follow the trail: @WhereMyDollarGo"
                    ]
                }
            ],
            "schedule_iso": dt_midday.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": ["gasprices", "economy", "moneybreakdown", "wheremydollargo", "finance"]
        },
        {
            "id": "short_003_deductible_vs_max",
            "title": "Deductible vs Out-of-Pocket Max in 40 Seconds",
            "script": (
                "Most people think hitting their health insurance deductible means medical care becomes completely free. "
                "That single mistake costs Americans thousands of dollars every year. "
                "Here is how it actually works. Your deductible is the starting line: you pay one hundred percent until you reach it. "
                "Then coinsurance begins, where the insurer splits the bill, usually eighty-twenty. "
                "Care only becomes one hundred percent free once you hit your out-of-pocket maximum. "
                "Remember: your deductible is where coverage starts; your maximum is where your payments end. "
                "Subscribe to WhereMyDollarGo for more!"
            ),
            "scenes": [
                {
                    "title": "Deductible vs Out-of-Pocket Max",
                    "subtitle": "The 3 Stages of Health Insurance",
                    "metric_label": "Stage 1: The Deductible",
                    "metric_val": "You Pay 100%",
                    "details": [
                        "You pay every dollar up to deductible limit",
                        "Insurance covers $0 until this is satisfied",
                        "The starting line of your policy coverage"
                    ]
                },
                {
                    "title": "Stage 2: Coinsurance Window",
                    "subtitle": "The Cost-Sharing Phase",
                    "metric_label": "The 80 / 20 Split",
                    "metric_val": "You Pay 20%",
                    "details": [
                        "Insurance pays 80% of allowed charges",
                        "You pay 20% coinsurance plus copays",
                        "Applies to all covered in-network claims"
                    ]
                },
                {
                    "title": "Stage 3: Out-of-Pocket Maximum",
                    "subtitle": "The True Financial Safety Net",
                    "metric_label": "The Finish Line",
                    "metric_val": "Insurer Pays 100%",
                    "details": [
                        "Absolute legal cap on covered in-network costs",
                        "Once reached, you pay $0 for the rest of year",
                        "Deductibles, copays, and coinsurance count"
                    ]
                },
                {
                    "title": "The Golden Rule of Insurance",
                    "subtitle": "Never Confuse the Two",
                    "metric_label": "Summary Takeaway",
                    "metric_val": "Start vs Finish",
                    "details": [
                        "Deductible = Where help starts",
                        "Out-of-Pocket Max = Where your bills stop",
                        "General education: @WhereMyDollarGo"
                    ]
                }
            ],
            "schedule_iso": dt_evening.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "tags": ["insurance", "healthcare", "deductible", "moneytips", "wheremydollargo"]
        }
    ]

    print("==================================================================")
    print("  WhereMyDollarGo: Generating & Scheduling 1st Batch of 3 Videos  ")
    print("==================================================================")

    results = []
    for item in batch:
        mp4_path = ROOT / "renders" / f"{item['id']}.mp4"
        render_short_video(
            topic_id=item["id"],
            script_text=item["script"],
            scenes_spec=item["scenes"],
            output_mp4=mp4_path
        )

        # Upload & schedule to YouTube
        print(f"\n[YOUTUBE] Uploading '{item['title']}'...")
        yt_id = upload_to_youtube(
            video_path=str(mp4_path),
            title=item["title"],
            description=item["script"],
            tags=item["tags"],
            publish_at_iso=item["schedule_iso"]
        )

        results.append({
            "id": item["id"],
            "title": item["title"],
            "schedule": "NOW (Immediate)" if not item["schedule_iso"] else f"Scheduled: {item['schedule_iso']}",
            "youtube_id": yt_id
        })

    print("\n==================================================================")
    print("                    1ST BATCH COMPLETED!                          ")
    print("==================================================================")
    for r in results:
        print(f"• {r['title']} -> {r['schedule']} (Video ID: {r['youtube_id']})")

if __name__ == "__main__":
    run_batch()
