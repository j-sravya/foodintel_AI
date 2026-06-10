# Food Sales Prep AI

This project is a food-industry sales prep assistant. It helps a salesperson prepare before meeting a restaurant, hotel, cafe, cloud kitchen, retailer, distributor, or QSR chain.

> Design an AI-powered agent to automatically curate and deliver timely, contextual company insights sourced from financial data, news, and social media to sales representatives before meetings, so that they are better informed and reduce manual research time.

## What the prototype does

- Applies the problem statement to two realistic sales-prep contexts in India-first QSR:
  - Internal QSR representatives preparing for aggregator, supplier, franchise, or leadership meetings.
  - External partner/vendor sales representatives preparing to approach a QSR account using only public and permissioned data.
- Opens directly into a simple salesperson flow:
  - Prep a prospect
  - Review the meeting script
  - Draft the follow-up
  - Use chain-account brief only when the prospect is a larger QSR chain
- Lets a sales representative select from 7 India-relevant QSR/operator accounts:
  - Jubilant FoodWorks - Domino's India
  - Westlife Foodworld - McDonald's India West & South
  - Devyani International - KFC, Pizza Hut, Costa Coffee
  - Restaurant Brands Asia - Burger King India
  - Sapphire Foods India - KFC and Pizza Hut
  - Barbeque-Nation Hospitality
  - Wow! Momo Foods
- Combines public company/brand context, recent public signals, representative customer/social themes, and role-safe QSR operating signals.
- Hides private outlet sales, inventory, POS, loyalty, menu-margin, and outlet-health signals from the external partner login.
- External signals include official company pages, annual reports, stock-exchange filings, and official brand/store pages with source URLs and verification labels.
- Shows outlet-level sales, stock, menu, and health data only in the internal QSR login as simulated own-company demo signals.
- Uses separate Streamlit pages for:
  - Meeting Brief
  - Prospect Research Agent
  - Meeting Planner
  - Account Signals
  - External Signals
  - Sales Playbook
  - Share Pack
  - Pilot Plan
  - ROI Calculator
  - Follow-Up
  - Stakeholders
  - Chatbot
- Adds all high-credibility features from the 80%+ real-world suitability list:
  - What Can I Share? Guardrail
  - Public Source Evidence Center
  - Meeting Type Planner
  - External Entity Alignment
  - Internal Partner Meeting Brief
  - Redacted Share Pack
  - Permissioned Pilot Plan Builder
  - Follow-Up Email Generator
  - Stakeholder Map
  - ROI / Impact Calculator
  - Objection Handler
- Reuses the old restaurant-operations features as internal QSR sales/partnership intelligence signals:
  - sales trend
  - inventory risk
  - menu performance
  - outlet health
  - demand forecast
  - competitor context
- Generates a pre-meeting brief with:
  - executive summary
  - account status
  - likely QSR pain points
  - account intelligence signals
  - recommendation reasoning and confidence/limitation notes
  - real-vs-demo data labels
  - source-proof table
  - suggested talking points
  - discovery questions
  - recommended solution angle
  - downloadable brief
- Adds a Prospect Research Agent for food-industry sales reps to enter a restaurant, hotel, cloud kitchen, retailer, distributor, or manufacturer prospect and generate:
  - lead score and lead tier
  - product-fit recommendation
  - likely pain points
  - stakeholder map
  - discovery questions
  - objection handling
  - proof plan
  - follow-up draft
- Adds source proof cards in External Signals with claim, source, source type, last checked date, meeting use, and source URL.
- Adds safe-sharing rules in Share Pack: safe to say, ask permission first, do not say, and customer-friendly wording.
- Adds pilot evidence requirements so every recommendation shows what proof is needed before production use.
- Includes a cost-aware sales-rep chatbot grounded on the selected project/account data. It first analyzes the question, then chooses the cheapest safe route:
  - Local app answer for greetings, meanings, calculations, source links, model summaries, and data-boundary questions.
  - LLM-only answer for deeper custom wording, pitch writing, and synthesis.
  - LLM + web search only when the question asks for latest/current/search/online verification.
- External partner flow supports entity alignment for aggregator/delivery platforms, packaging suppliers, POS/CRM/analytics vendors, logistics partners, food ingredient suppliers, and marketing/loyalty agencies.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

You can also store the key locally in `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your_key_here"
OPENAI_CHATBOT_MODEL = "gpt-4.1"
```

Do not paste the key into app code. The project ignores `.streamlit/secrets.toml` through `.gitignore`.

The dashboard pages use local sample data in `data/company_signals.json`. The Chatbot page can answer simple local questions without an API key. `OPENAI_API_KEY` is required only for LLM-only and LLM + web-search routes.

Optional model override:

```bash
export OPENAI_CHATBOT_MODEL="gpt-4.1"
```

## Walkthrough

- Written explanation: `APP_WALKTHROUGH.md`
- Animated walkthrough: `assets/qsr_accountbrief_walkthrough.gif`

## 40/40 submission readiness

The software is only one part of the 40-mark submission. The guideline also expects real evidence such as interviews, screenshots, Jira proof, channel tests, and an MVP recording.

- Evidence templates: `40_40_EVIDENCE_PACK/`
- Rubric map: `40_40_EVIDENCE_PACK/GRADING_RUBRIC_MAP.md`
- Evidence tracker CSV: `40_40_EVIDENCE_PACK/evidence_tracker.csv`
- Phase-by-phase submission: `QSR AccountBrief AI - Phase by Phase Submission.docx`
- Evidence pack Word builder: `build_40_40_evidence_pack_doc.py`

Do not submit the final PDF with `TO FILL` or `Final evidence to attach` placeholders. Replace them with real recording links, screenshot links, source links, team names, and student codes/IDs before export.
