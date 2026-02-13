# 🤖 MAYAI Job Application Pipeline

**Autonomous AI-powered job search and application system for Data Analyst roles.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Autonomous%20Agent-green.svg)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📋 Overview

An intelligent automation pipeline that streamlines the job search process by:
- 🔍 **Discovering** 50+ job opportunities daily via Brave Search API
- 📊 **Scoring** matches with AI-powered relevance algorithm (80%+ threshold)
- 📄 **Generating** tailored resumes and cover letters for each application
- 📓 **Tracking** all applications in a structured Notion database
- 🔔 **Alerting** via Telegram for urgent opportunities (recruiters, interviews)

**Human-in-the-loop:** All applications require manual approval before submission.

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Search    │────▶│    Score    │────▶│   Generate  │
│(Brave API)  │     │  (AI Match) │     │ (Templates) │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                       ┌────────────────────────┘
                       ▼
              ┌─────────────────┐
              │  Human Review   │
              │  & Approval     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │    Submit       │
              │  (Manual)       │
              └─────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenClaw installed
- API keys (see Configuration)

### Installation

```bash
# Clone the repository
git clone https://github.com/vrajeshbhatt/job-application-pipeline.git
cd job-application-pipeline

# Install dependencies
pip install -r requirements.txt

# Configure API keys (see below)
# Run initial search
python scripts/job_search.py
```

### Configuration

Create `credentials/` directory with your API keys:

```
credentials/
├── brave-search.md      # Brave Search API key
├── notion.md            # Notion integration token
├── elevenlabs.md        # ElevenLabs API key (optional)
└── google-workspace.md  # Gmail OAuth (optional)
```

**Note:** The `credentials/` folder is git-ignored for security.

---

## 📊 Features

### 1. Intelligent Job Search
- **Sources:** LinkedIn, Indeed, Job Bank Canada, company career pages
- **Target:** Entry-level Data Analyst roles (1-2 years experience)
- **Location:** Atlantic Canada (NS, NB, PEI, NL) priority, Ontario secondary
- **Frequency:** Daily at 6:00 AM EST

### 2. Smart Match Scoring
```
Match Score = (Location × 40%) + (Skills × 30%) + (Company × 20%) + (Salary × 10%)
```

Only jobs scoring **80%+** are processed.

### 3. Dynamic Resume Tailoring
- HTML templates with variable substitution
- Keyword optimization for ATS
- Achievement highlighting based on job requirements
- Automatic PDF generation

### 4. Application Tracking
Notion database with fields:
- Company, Role, Location
- Match Score, Status
- Application Date, Resume/Cover Letter links
- Follow-up reminders

---

## 📁 Project Structure

```
.
├── applications/           # Generated application packages
│   └── Company_Role/
│       ├── resume.html
│       ├── cover_letter.html
│       └── job_details.txt
├── docs/                   # Documentation
│   ├── job_application_pipeline.md
│   ├── linkedin_post_draft.md
│   └── architecture_diagram.md
├── templates/              # Base templates
│   ├── resume_template.html
│   └── cover_letter_template.html
├── scripts/                # Automation scripts
│   ├── job_search.py
│   ├── resume_generator.py
│   └── notion_sync.py
├── credentials/            # 🔒 API keys (git-ignored)
├── job_search_tracker.md   # Manual tracking backup
└── README.md              # This file
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Search Engine** | Brave Search API |
| **LLM** | OpenRouter (Kimi K2.5) |
| **Voice** | ElevenLabs |
| **Database** | Notion API |
| **Notifications** | Telegram Bot API |
| **Scheduler** | OpenClaw Cron |
| **Language** | Python 3.11+ |

---

## 🔐 Security

- ✅ All API keys stored in `credentials/` (git-ignored)
- ✅ No hardcoded secrets in source code
- ✅ Environment variables for production
- ✅ Regular token rotation

---

## 📈 Results

| Metric | Value |
|--------|-------|
| Jobs Found | 50+ |
| Match Rate | 15% above 80% threshold |
| Templates Created | 2 tailored packages |
| Time Saved | ~3 hours/day |
| API Cost | $0 (free tiers) |

---

## 🎯 Sample Applications

### 1. Province of Nova Scotia - Data Analyst (90% match)
- Government role, program evaluation focus
- Full application package generated

### 2. Altus Group - Analyst, Valuation & Advisory (85% match)
- Real estate data analysis
- Entry-level friendly

See `applications/` folder for complete examples.

---

## 🤝 Contributing

This is a personal project, but feedback is welcome! Open an issue for:
- Bug reports
- Feature suggestions
- Documentation improvements

---

## 📝 License

MIT License - feel free to adapt for your own job search!

---

## 🙏 Acknowledgments

- [OpenClaw](https://openclaw.ai) - Autonomous agent framework
- [Brave Search](https://brave.com/search/api/) - Privacy-focused search API
- [Notion](https://notion.so) - Database & documentation

---

## 📞 Contact

**Vrajesh Bhatt**
- 📧 vrajesh.bhatt@outlook.com
- 💼 [LinkedIn](https://linkedin.com/in/vrajeshbhatt)
- 🐙 [GitHub](https://github.com/vrajeshbhatt)

---

*Built with 💙 and lots of coffee while job searching.*
