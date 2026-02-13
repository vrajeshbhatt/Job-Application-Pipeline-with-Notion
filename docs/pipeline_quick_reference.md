# Job Application Pipeline - Quick Reference

## 🎯 One-Pager

```
┌────────────────────────────────────────────────────────────────┐
│              MAYAI JOB APPLICATION PIPELINE                     │
│                     (Daily 6:00 AM EST)                        │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  STEP 1: SEARCH         STEP 2: SCORE        STEP 3: GENERATE │
│  ┌──────────┐          ┌──────────┐          ┌──────────┐     │
│  │  Brave   │─────────▶│   AI     │─────────▶│ Resume   │     │
│  │  Search  │  50 jobs │  Match   │  80%+    │ Tailor   │     │
│  │   API    │          │  Score   │          │ Engine   │     │
│  └──────────┘          └──────────┘          └──────────┘     │
│       │                      │                    │            │
│       ▼                      ▼                    ▼            │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                    STEP 4: TRACK                        │   │
│  │  • Notion Database (Company, Role, Status, Match %)     │   │
│  │  • Application PDFs (Resume + Cover Letter)            │   │
│  └────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                           ▼                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │                 STEP 5: NOTIFY                          │   │
│  │  • Telegram Alert (Summary of new opportunities)       │   │
│  │  • Urgent emails prioritized                           │   │
│  └────────────────────────────────────────────────────────┘   │
│                           │                                    │
│                           ▼                                    │
│  ┌────────────────────────────────────────────────────────┐   │
│  │              STEP 6: HUMAN REVIEW                       │   │
│  │  ✅ Review tailored application                         │   │
│  │  ✅ Approve or modify                                   │   │
│  │  ✅ Submit manually (no auto-submit for privacy)       │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## 📊 Key Stats

| Metric | Value |
|--------|-------|
| **Jobs Found/Day** | 15-25 |
| **Match Threshold** | 80%+ |
| **Time Saved** | ~3 hours/day |
| **Automation Level** | 90% (human approval required) |
| **API Cost** | $0 (free tiers) |

## 🛠️ Tech Stack

```
Search:     Brave Search API
LLM:        OpenRouter (Kimi K2.5)
Voice:      ElevenLabs
Tracking:   Notion API
Notify:     Telegram Bot
Scheduler:  OpenClaw Cron
Language:   Python 3.11+
```

## 🔐 Security

```
credentials/
├── brave-search.md      # 🔒 Git-ignored
├── notion.md            # 🔒 Git-ignored
└── elevenlabs.md        # 🔒 Git-ignored

✅ No secrets in source code
✅ Environment variables in production
✅ Regular token rotation
```

## 📁 File Locations

```
applications/
├── CompanyName_Role/
│   ├── resume.html
│   ├── cover_letter.html
│   └── job_details.txt

templates/
├── resume_template.html
└── cover_letter_template.html

scripts/
├── job_search.py
├── resume_generator.py
└── notion_sync.py
```

## 🎯 Target Profile

- **Role:** Entry-level Data Analyst
- **Experience:** 1-2 years
- **Location:** Atlantic Canada (NS, NB, PEI, NL)
- **Skills:** Python, SQL, Power BI, Data Analysis

## ⚡ Quick Start

1. Configure API keys in `credentials/`
2. Customize `templates/` with your info
3. Set target locations in `config.json`
4. Run initial search: `python job_search.py`
5. Review generated applications
6. Approve and submit!

---

*Part of the MAYAI autonomous agent ecosystem.*
