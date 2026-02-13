# 🤖 MAYAI Job Application Pipeline
## Autonomous AI-Powered Job Search & Application System

---

## 📋 Executive Summary

The **MAYAI Job Application Pipeline** is an autonomous AI system designed to streamline the job search process for Data Analyst roles. Built with Python and integrated with multiple APIs, it automates job discovery, resume tailoring, and application tracking while maintaining human oversight for final submissions.

**Key Capabilities:**
- 🔍 Automated job search across multiple platforms
- 📄 AI-powered resume & cover letter customization
- 📊 Smart match scoring (80%+ relevance filtering)
- 📓 Automated tracking in Notion database
- 🔔 Real-time notifications via Telegram
- 🔐 Secure credential management

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    JOB APPLICATION PIPELINE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   SCHEDULER  │───▶│    SEARCH    │───▶│    SCORE     │     │
│  │  (Cron Job)  │    │  (Brave API) │    │   (AI Match) │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│         │                                            │          │
│         ▼                                            ▼          │
│  ┌──────────────┐                         ┌──────────────┐     │
│  │   NOTIFIER   │                         │   GENERATE   │     │
│  │  (Telegram)  │                         │ (Templates)  │     │
│  └──────────────┘                         └──────────────┘     │
│                                                    │            │
│                                         ┌──────────────┐       │
│                                         │    UPLOAD    │       │
│                                         │   (Notion)   │       │
│                                         └──────────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Search Engine** | Brave Search API | Job discovery across web |
| **LLM** | OpenRouter (Kimi K2.5) | Resume tailoring & cover letters |
| **TTS** | ElevenLabs | Voice briefings |
| **Notifications** | Telegram Bot API | Real-time alerts |
| **Database** | Notion API | Application tracking |
| **Scheduler** | OpenClaw Cron | Automated execution |
| **Language** | Python 3.11+ | Core automation logic |

---

## 📁 Project Structure

```
workspace/
├── 📂 applications/              # Generated application packages
│   ├── CompanyName_Role/
│   │   ├── resume.html          # Tailored resume
│   │   ├── cover_letter.html    # Custom cover letter
│   │   └── job_details.txt      # Match score & metadata
│   └── ...
│
├── 📂 templates/                 # Base templates
│   ├── resume_template.html     # Professional resume template
│   └── cover_letter_template.html
│
├── 📂 credentials/               # 🔒 Secure API keys (git-ignored)
│   ├── brave-search.md          # Brave API credentials
│   ├── notion.md                # Notion integration token
│   └── ...
│
├── 📂 scripts/                   # Automation scripts
│   ├── job_search.py            # Main search pipeline
│   ├── resume_generator.py      # Tailoring engine
│   └── notion_sync.py           # Database sync
│
├── 📄 job_search_tracker.md     # Manual tracking backup
└── 📄 job_leads_top_8.json      # Priority opportunities
```

---

## 🔍 Job Search & Discovery

### Search Parameters
- **Role:** Entry-level Data Analyst (1-2 years experience)
- **Location:** Atlantic Canada (NS, NB, PEI, NL), Ontario secondary
- **Sources:** LinkedIn, Indeed, Job Bank Canada, Company Career Pages
- **Match Threshold:** 80%+ relevance score

### Match Scoring Algorithm
```python
Match Score = (Location × 40%) + (Skills × 30%) + (Company × 20%) + (Salary × 10%)
```

**High-Priority Indicators:**
- ✅ Halifax/Dartmouth location
- ✅ Entry-level friendly language
- ✅ Python, SQL, Power BI requirements
- ✅ Recent posting (< 7 days)

---

## 📄 Resume & Cover Letter Generation

### Dynamic Tailoring Process

1. **Job Parsing:** Extract key requirements from posting
2. **Skill Mapping:** Match candidate skills to job needs
3. **Keyword Optimization:** Insert relevant ATS keywords
4. **Achievement Highlighting:** Prioritize relevant accomplishments
5. **Output Generation:** Create HTML → PDF application package

### Template Variables
```html
<!-- Resume -->
<h1>{{candidate_name}}</h1>
<p>{{professional_summary_customized}}</p>

<!-- Cover Letter -->
<p>Dear Hiring Manager,</p>
<p>I am writing to express interest in {{job_title}} at {{company_name}}...</p>
```

---

## 📊 Application Tracking

### Notion Database Schema

| Field | Type | Description |
|-------|------|-------------|
| **Company** | Title | Employer name |
| **Role** | Text | Job title |
| **Location** | Select | Province/City |
| **Match Score** | Number | 0-100% relevance |
| **Status** | Select | Applied / Interview / Offer / Rejected |
| **Date Applied** | Date | Submission date |
| **Resume Link** | URL | Tailored resume PDF |
| **Cover Letter** | URL | Custom cover letter |
| **Job URL** | URL | Original posting |
| **Notes** | Text | Follow-up reminders |

### Automated Status Updates
- 🟡 **New Lead** → Auto-added from search
- 🔵 **Ready to Apply** → Resume generated
- 🟢 **Applied** → Manual confirmation
- 🟠 **Follow-up** → Reminder scheduled

---

## 🔐 Security & Credential Management

### Sensitive Data Handling

**All API keys stored in:**
```
credentials/
├── brave-search.md      # BSAY... (masked)
├── notion.md            # ntn_... (masked)
├── elevenlabs.md        # sk_... (masked)
└── github.md            # ghp_... (masked)
```

**Security Measures:**
- ✅ `.gitignore` excludes `credentials/` from version control
- ✅ Environment variables for production deployment
- ✅ Token rotation every 90 days
- ✅ No hardcoded secrets in source code

---

## 🚀 Deployment & Automation

### Cron Schedule
```json
{
  "job_search": "0 6 * * *",      // Daily at 6 AM EST
  "resume_tailoring": "0 7 * * *", // Daily at 7 AM EST
  "notion_sync": "0 */6 * * *",    // Every 6 hours
  "gmail_monitor": "*/30 * * * *"  // Every 30 minutes
}
```

### Execution Flow
1. **6:00 AM** → Search for new jobs
2. **6:15 AM** → Score and filter (80%+ only)
3. **6:30 AM** → Generate tailored resumes
4. **7:00 AM** → Send Telegram summary
5. **Manual** → User reviews and approves applications

---

## 📈 Performance Metrics

### Current Pipeline Results
- **Jobs Found:** 50+ opportunities
- **Match Rate:** 15% above 80% threshold
- **Templates Created:** 2 tailored packages
- **Time Saved:** ~3 hours/day vs manual search

### Success Tracking
- Application-to-Interview ratio
- Response rate by company size
- Match score correlation with callbacks

---

## 🎯 Future Enhancements

**Phase 2 Roadmap:**
1. **LinkedIn API Integration** → Direct job pulling
2. **Auto-Apply Feature** → One-click submissions (with approval)
3. **Interview Prep** → AI-generated Q&A based on company
4. **Salary Tracking** → Market rate analysis
5. **Network Analysis** → Mutual connections at target companies

---

## 🙏 Acknowledgments

Built with:
- [OpenClaw](https://openclaw.ai) — Autonomous agent framework
- [Brave Search API](https://brave.com/search/api/) — Privacy-focused search
- [ElevenLabs](https://elevenlabs.io) — Voice synthesis
- [Notion](https://notion.so) — Database & documentation

---

## 📞 Connect

**Vrajesh Bhatt**
- 📧 vrajesh.bhatt@outlook.com
- 💼 linkedin.com/in/vrajeshbhatt
- 🐙 github.com/vrajeshbhatt

---

*This pipeline demonstrates the practical application of AI automation in career development while maintaining human oversight and decision-making.*

**#JobSearch #DataAnalyst #AIAutomation #CareerDevelopment #Python #OpenSource**
