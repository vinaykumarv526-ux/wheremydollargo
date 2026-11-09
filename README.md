# 💵 WhereMyDollarGo: Autonomous 24/7 Cloud Production Engine

[![Daily Pipeline](https://github.com/vinaykumarv526-ux/wheremydollargo/actions/workflows/daily_pipeline.yml/badge.svg)](https://github.com/vinaykumarv526-ux/wheremydollargo/actions/workflows/daily_pipeline.yml)
[![Weekly Report](https://github.com/vinaykumarv526-ux/wheremydollargo/actions/workflows/weekly_report.yml/badge.svg)](https://github.com/vinaykumarv526-ux/wheremydollargo/actions/workflows/weekly_report.yml)

> **Channel Handle**: `@WhereMyDollarGo`  
> **Tagline**: *Every dollar, explained.*  
> **Target Audience**: US adults (22–45), earners, renters, first-time home buyers, young families.

This repository runs an **entirely automated, cloud-hosted content engine** for YouTube Shorts, long-form explainers, and daily carousels. **You do not need to keep your laptop running.** Everything executes automatically on scheduled GitHub Actions cloud runners.

---

## 📅 Weekly Review Routine (Check Once a Week)

You only need to check in once a week from your phone or browser:
1. **GitHub Issues**: Every Sunday, an automated issue titled `Weekly Channel Status & Health Report: YYYY-MM-DD` is created with a complete breakdown of what was generated and scheduled.
2. **Weekly Report File**: Read [`weekly-report.md`](weekly-report.md) directly on GitHub.
3. **Publish Queue**: Check the [`publish-queue/`](publish-queue/) folder to view all generated scripts, metadata, and carousels.

---

## ⚡ Autonomous Cloud Schedule (All Managed via GitHub Actions)

| Trigger / Cron | What Runs in the Cloud | Output |
|---|---|---|
| **Daily at 06:00 UTC** | `buffer_scheduler.py` | Generates & stages the morning Short and runs `daily_carousel.py` |
| **Daily at 16:00 UTC** | `buffer_scheduler.py` | Generates & stages the evening peak-hour Short |
| **Every Sunday at 00:00 UTC** | `weekly_reporter.py` | Compiles weekly audit, updates `weekly-report.md`, and creates a GitHub issue |

---

## 🔐 Optional: 100% Direct YouTube API Auto-Publishing

By default, the pipeline stages all scripts, descriptions, and carousels into `publish-queue/` and commits them to the repo so you can inspect them.

To enable **direct automatic scheduling to YouTube Studio**:
Add the following three Secrets in your repo at **Settings → Secrets and variables → Actions**:
1. `YT_CLIENT_ID`
2. `YT_CLIENT_SECRET`
3. `YT_REFRESH_TOKEN`

Once added, the pipeline will directly upload and schedule the videos into YouTube Studio on private/scheduled status at US peak viewing hours (12:00 PM ET & 6:00 PM ET).

---

## 📂 Repository Directory Structure

```
├── .github/
│   └── workflows/
│       ├── daily_pipeline.yml       # Cloud cron: runs daily generation & maintains 2-day buffer
│       └── weekly_report.yml        # Cloud cron: runs every Sunday to produce weekly status
├── assets/
│   ├── avatar.jpg                   # Channel icon (1:1 high contrast vector logo)
│   └── banner.jpg                   # Channel banner (2560x1440 widescreen)
├── automation/
│   └── pipeline/
│       ├── topics.json              # Structured queue of 15+ verified US finance topics
│       ├── state.json               # Buffer tracker, published slot logs, next index
│       ├── buffer_scheduler.py      # Core automated generator & queue manager
│       ├── daily_carousel.py        # Daily 5-slide macro-finance carousel generator
│       ├── weekly_reporter.py       # Weekly audit & GitHub issue generator
│       └── uploader.py              # YouTube API OAuth2 direct scheduler
├── publish-queue/                   # Dated folders containing ready-to-publish assets
├── sources.md                       # Primary source citations (IRS, BLS, Fed, SSA, EIA)
├── styles-used.md                   # Style rotation log (enforcing 20-video freshness)
├── content-plan.md                  # Comprehensive 30-day master roadmap
└── CLAUDE.md                        # Production agent master prompt configuration
```
