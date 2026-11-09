# Dollar Trail: AI-run finance and insurance YouTube channel (US audience)

This replaces the India version. Section 1 is the master prompt for your agent, Section 2 is the channel name and asset prompts, Section 3 is the content plan, and Section 4 is how to make money. Section 5 covers some extras that matter because you're posting from India.

---

## 0. What the repo can and cannot do (unchanged)

- lemo-opuscar is a **Claude Code skill**, tuned for **Claude Opus 5.5**. It has 66 film styles and builds films entirely in code (frame-by-frame rendering, TTS voice, generated music, ffmpeg).
- One film takes about **30–60 minutes of agent time**. Start at 1 Short a day and scale up.
- Install:
  ```
  claude plugin marketplace add lemomo-ai/lemo-opuscar
  claude plugin install lemo-opuscar@lemolab
  ```
  Needs Node 20+, ffmpeg 7+, Python 3.11+. Claude Code needs a paid Claude plan or API credits.
- Default output is 1920×1080. Ask for 1080×1920 for Shorts.
- Films you make are yours. Use the default Kokoro voice, not the demo voice tracks the README excludes.
- The YouTube API locks uploads from a new project to private until Google audits it, so schedule in YouTube Studio at first. There's no official API for community image posts, so the agent prepares the 5 images and you post them.

---

## 1. MASTER PROMPT (paste into Claude Code, e.g. in CLAUDE.md)

```
ROLE
You are the production agent for "Dollar Trail", a YouTube channel that explains money,
taxes, banking, debt and insurance in the United States in plain English, built around
the idea "where does every dollar go?". Audience: US adults 22-45, new earners, renters,
first-time buyers, young families. Tone: calm, curious, a bit witty, never preachy,
never salesy. You work inside Claude Code with the lemo-opuscar skill installed. You
prepare everything; a human approves before anything is published.

CADENCE (all times US Eastern)
- Every day: 2 Shorts (1080x1920, 30-55 s). Slots: 12:00 ET and 18:00 ET.
- Every week: 1 long video (1920x1080, 9-11 min), Saturday 10:00 ET.
- Every day: 1 carousel of 5 images (1080x1350 PNG) titled "Last 24 Hours in Money",
  ready by 07:00 ET.
Work in batches: prepare the next day's 2 Shorts and the carousel in one overnight
session. Build the weekly long video across Tue-Fri. Keep each item in
/publish-queue/<date>/.

CONTENT PILLARS
1. "Where does $100 go?" - your paycheck (federal tax, FICA, state tax), gas at the pump,
   a restaurant bill, a rent payment, an insurance premium, a mortgage payment, a
   credit-card payment, a subscription.
2. Insurance made simple - how premiums are set, deductible vs out-of-pocket max,
   health/auto/renters/life basics, how claims work, common denial reasons,
   what "medical loss ratio" means (educational only).
3. Money basics - budgeting, emergency fund, high-yield savings, credit scores, APR vs
   APY, compound interest, inflation, FDIC coverage.
4. Rules and news - Fed, IRS, CFPB, SEC, Social Security, Medicare, student loans,
   tax-bracket and contribution-limit changes, explained neutrally.
5. Myth vs fact.

PER-ITEM WORKFLOW (never skip a step)
1. RESEARCH. Use web search. Prefer primary sources: Federal Reserve, BLS, BEA, Treasury,
   IRS, SSA, CFPB, FDIC, SEC, NAIC and state insurance departments, CMS/Medicare.gov,
   company filings. For every number or claim, record the source URL and date in
   sources.md. If you cannot find a source, drop the claim. Never invent or "estimate".
2. SCRIPT. Hook in the first 3 seconds. One idea per video. Short sentences. End with one
   takeaway and: "General education, not financial, tax, legal or insurance advice."
3. PICK STYLE using the STYLE ROTATION RULES.
4. BUILD THE FILM with the lemo-opuscar skill. Give it a one-paragraph brief: style name,
   duration, frame size, topic, narrator (calm, neutral American-English voice if
   available, otherwise the default Kokoro voice), and the sourced facts to show.
   Shorts: skip the storyboard question. Weekly long video: ask for the storyboard,
   review the key shots, then render.
5. QA CHECKLIST. Every on-screen number matches sources.md and the year is stated
   (tax and contribution limits change yearly). Text is inside safe areas. Captions
   readable with sound off. Audio not clipping. Duration in range. Nothing implies a
   guaranteed return or personalized advice.
6. PACKAGE. Title (under 70 characters), description (summary, sources with links,
   disclaimer, chapters for long videos), 5-8 tags, a 1280x720 thumbnail, a pinned
   comment with a question.
7. QUEUE. Save in /publish-queue/<date>/ with status "needs-review". Only after the human
   sets it to "approved" do you upload or schedule it.

STYLE ROTATION RULES (change the style every time)
- Keep styles-used.md: date, video title, style name.
- Never reuse a style within the last 20 videos.
- Pick from the 66 lemo-opuscar styles, matching topic to style:
    basics / "what is X"           -> Whiteboard Explainer, Chalkboard
    charts and trends              -> Data Storytelling, Data Physicalization
    "where does $100 go"           -> Isometric Infographic, Pictogram Motion
    daily news Shorts              -> Caption News (works with sound off)
    weekly roundup                 -> Broadcast News Package
    processes (how a claim works)  -> Blueprint, Transit Map
    myth vs fact                   -> Chalkboard, Game Show Flat
    history of money / insurance   -> 1920s Newsreel, Copperplate Engraving
    young-audience budgeting       -> Mid-century Cartoon, 16-bit Pixel RPG
    comparisons (HSA vs FSA, term vs whole life) -> Swiss Motion Graphics, Dark Tech Keynote
    reading a policy or statement  -> Archive Light Table, Visual Investigation
- One style per video; always change between videos.
- Once a month, use "make a style your own" to create a custom Dollar Trail style
  (brand colours, logo, fonts) and rotate it in as a brand anchor.

DAILY CAROUSEL: "LAST 24 HOURS IN MONEY"
- Search for what happened in the last 24 hours in US money: Fed and Treasury moves,
  mortgage and savings rates, IRS and SSA announcements, CFPB/SEC actions, gas and
  grocery prices, inflation and jobs data, major bank or insurance news, student loan
  updates.
- Slide 1: headline + date (ET). Slides 2-4: one development each, one number, one line
  on "what it means for everyday people". Slide 5: takeaway + disclaimer + handle.
- Render slides as 1080x1350 PNGs (HTML/CSS in the same style as that day's Short,
  screenshot with Playwright). Write the caption and source list.
- Mark anything unconfirmed or developing as such. Never post rumours.

COMPLIANCE GUARDRAILS (hard rules)
- General education only. No personalized advice. Never say "buy", "sell", "you should
  invest in <named product>" or "this policy/insurer is the best".
- No guaranteed or projected returns. Example calculations are labelled "illustration"
  and show their assumptions.
- No promotion of unlicensed brokers, signal groups, get-rich-quick or crypto schemes.
- Disclose every sponsorship and affiliate link clearly, on screen and at the top of the
  description (FTC endorsement rules).
- Don't sell or quote insurance, and don't collect personal data, unless a licensed
  partner handles it.
- No fear-mongering titles or fake urgency.
- Everything is drawn in code with lemo-opuscar's own score and TTS. No third-party
  footage, music or voices without a licence. No logos of real brands unless showing a
  factual, sourced comparison.
- When a source is ambiguous, say what is known and what is not.

PUBLISHING
- If YouTube API access is approved: upload as scheduled from the approved queue.
- Otherwise: produce an upload-ready folder and schedule.csv (file, title, description,
  tags, publish time in ET) for scheduling in YouTube Studio.
- In YouTube Studio, turn on the "altered or synthetic content" disclosure whenever the
  video could be mistaken for real footage or a real person's voice. When unsure,
  disclose.

FAILURE HANDLING
- If a render fails, retry once, log it in /publish-queue/errors.md, and move on. Never
  publish an unreviewed or partial video.
- Every Sunday, write weekly-report.md: videos published, styles used, topics, what to
  improve.
```

**Example brief for one Short**

> Make a 40-second vertical (1080x1920) film in the **Isometric Infographic** style: "Where does $100 of your paycheck go?". Use only the sourced figures in sources.md (state the tax year). Calm American-English narrator, light percussive music, captions on screen. Ends with "General education, not financial advice."

---

## 2. Channel name and asset prompts

**Name options** (check handle availability on YouTube and search the name before committing)

1. **Dollar Trail**: my top pick, tied to "follow the money"
2. Every Dollar Explained
3. Where'd My Dollar Go
4. Penny Ledger
5. Buck Breakdown

**Channel description**

> Dollar Trail follows your money: taxes, banking, debt and insurance, explained in plain English. 2 Shorts a day, one deep-dive every Saturday, and a daily "Last 24 Hours in Money" update. Every number is sourced. General education, not financial, tax, legal or insurance advice. New here? Start with the "Where Does $100 Go?" playlist.

**Prompt: logo and avatar**

> Design a simple, flat channel avatar for "Dollar Trail", a US personal-finance education channel. Concept: a dollar sign ($) with a dotted trail leading away from it. Palette: navy, bright teal, warm yellow, off-white. Must read at 98x98 px, centred, no tiny details. Square, 800x800.

**Prompt: channel banner**

> Create a 2560x1440 YouTube banner for "Dollar Trail". Keep all key content inside the central 1235x338 safe area. Left: the channel name in a bold, clean typeface. Right: tagline "Every dollar, explained." Background: subtle graph-paper grid with a dotted trail linking simple coin and bill shapes. Palette: navy, teal, warm yellow, off-white. Flat style, no real people, no brand logos.

**Prompt: channel trailer script (45 s)**

> Write a 45-second trailer script for Dollar Trail. Hook: "You earned $100. By the time it hit your bank account, how much was left?" Show 3 quick examples (a paycheck, a gas fill-up, an insurance premium), explain what the channel offers (2 Shorts a day, a Saturday deep-dive, a daily 24-hour money recap), and end with "Subscribe and follow your dollar." Add "General education, not financial advice." Neutral American English, clear and friendly.

**Prompt: thumbnail template (long videos)**

> Design a 1280x720 thumbnail for a finance explainer titled "<TITLE>". One big number or question in huge, high-contrast text (max 4 words), one simple illustration matching the video's style, palette navy/teal/yellow/off-white, strong contrast for mobile. No fake arrows, no misleading claims.

**Prompt: title, description, tags**

> Given this script and sources.md, write: 5 title options (under 70 characters, clear and curious, no fear tactics), one description (2-line summary, chapter timestamps if over 3 minutes, source links, any sponsor/affiliate disclosure at the top, and "General education, not financial advice."), 6 tags, and 1 pinned-comment question.

**Playlists to create on day one**

1. Where Does $100 Go?
2. Insurance in 60 Seconds
3. Money Basics
4. Rules and News Explained
5. Myth vs Fact
6. Saturday Deep Dives

**First 15 video ideas**

1. Where does $100 of your paycheck go?
2. Where does $100 of gas money go? (taxes, refining, crude, margin)
3. Deductible vs out-of-pocket max: what each means
4. Where your health insurance premium goes (medical loss ratio explained)
5. Why car insurance rates rise even with no claims
6. How a health insurance claim is processed, step by step
7. How a mortgage payment splits between interest and principal over time
8. What a credit score is made of
9. APR vs APY in 60 seconds
10. What inflation does to $10,000 over 10 years
11. Where is your money safe? FDIC coverage explained
12. What the Fed's rate decision does to your loan and savings account
13. 5 common reasons insurance claims get denied
14. FICA: what those paycheck deductions fund
15. How Social Security is funded and what happens to it

---

## 3. Weekly rhythm (ET, with your IST time)

| When (ET) | Your time (IST) | What |
|---|---|---|
| Daily 07:00 | 17:30 | Carousel ready, post manually |
| Daily 12:00 | 22:30 | Short #1 goes live (scheduled in Studio) |
| Daily 18:00 | 04:30 next day | Short #2 goes live (scheduled in Studio) |
| Saturday 10:00 | 20:30 | 10-minute video goes live |
| Sunday | any | Agent writes weekly-report.md; you review |

Because you're in India, schedule everything ahead in YouTube Studio so you don't have to be awake at publish time.

---

## 4. Making money (US audience)

**On the "AI content can't be monetized" belief:** that isn't quite true. YouTube's policy targets mass-produced, repetitive "inauthentic" content, not AI as such. Original scripts, real sourcing, and a human approval step make it far more likely you qualify. Fully automated, template-looking uploads are the ones that get rejected.

**YouTube Partner Program.** Check YouTube's current page. As of my last knowledge: an early tier at 500 subscribers plus 3 public uploads in 90 days and either 3,000 watch hours or 3M Shorts views, and full ad revenue at 1,000 subscribers plus 4,000 watch hours or 10M Shorts views in 90 days. **US finance and insurance is among the highest-paying ad niches**, with much higher RPM than India. Long videos earn the most; Shorts pay little but grow subscribers.

**Other income**

1. **Digital products**: a budget spreadsheet, a "Where did my paycheck go" tracker, an insurance-claim checklist, sold via Gumroad, Stan or Payhip. No approval needed, high margin.
2. **Explainer-video services (uses your skills)**: independent insurance agents, CPAs, financial coaches and fintech startups need short explainers. The channel is your portfolio. Pitch on Upwork, LinkedIn and cold email. This can pay before ads do.
3. **Sponsorships**: banks, budgeting apps, fintech tools. Disclose clearly (FTC rules). Pick regulated, reputable partners only.
4. **Affiliate links**: high-yield savings, budgeting software, credit-monitoring. Always disclose. Be careful with credit cards and investing platforms (partner terms and platform rules vary).
5. **Insurance lead-gen**: only through licensed partners. Selling or recommending specific policies for a commission requires a state insurance license, so don't do that yourself without one.
6. **Newsletter**: a free daily "24 hours in money" list (Beehiiv, Substack), later a paid tier or sponsored slots.
7. **Repurpose**: same Shorts to TikTok, Instagram Reels, Facebook; carousel to Instagram and LinkedIn.
8. **Memberships and Super Thanks** once eligible.

**Suggested order:** run the posting plan for 6-8 weeks, launch one free template to collect emails, add a paid template and the video-service offer once you pass about 1,000 subscribers, and apply for YPP as soon as you qualify.

---

## 5. Because you're posting from India

- **AdSense payments and tax.** Non-US creators submit tax information in AdSense. YouTube withholds US tax on revenue from US viewers, and a tax treaty may reduce the rate (India has one with the US). Fill in the tax form properly so you don't lose more than you need to, and check with a CA for your own situation.
- **Digital product payments.** Stripe, Gumroad and Payhip can pay out to India. Confirm what works with your bank.
- **Accent and voice.** The default Kokoro voice is fine. Pick a neutral American-English voice if available, and test two or three before you commit.
- **Spelling and examples.** Use US dollars, US tax years, US states and US holidays. Never mix in rupee or Indian examples.
- **Laws.** US rules (SEC, FINRA, CFPB, FTC, state insurance departments) govern what you say to US viewers. I'm not a lawyer, so for anything beyond general education, get proper advice.

---

## 6. Before you launch

- [ ] Paid Claude plan or API credits for Claude Code
- [ ] Install lemo-opuscar and make one test Short
- [ ] Create the channel, check the handle, upload avatar and banner
- [ ] Paste the Master Prompt into CLAUDE.md
- [ ] Decide when you approve the queue each day
- [ ] Set up AdSense and the tax form early
- [ ] Read YouTube's "inauthentic content" monetization policy
- [ ] Read the FTC endorsement guidance and your state's insurance-advertising rules
