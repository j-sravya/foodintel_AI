# QSR AccountBrief AI - App Walkthrough

## What The App Does

QSR AccountBrief AI is a pre-meeting intelligence app for sales and partnership representatives who are preparing for QSR business meetings in India first. It follows the original problem statement: an AI-powered agent curates timely company insights from financial data, news, social media, and account signals so representatives can prepare faster and enter meetings with better context.

The app now supports two realistic login types:
- Internal QSR representative: someone working inside the restaurant/QSR company, preparing for meetings with aggregators, suppliers, franchisees, or internal leadership.
- External partner/vendor representative: someone from outside the QSR, such as Swiggy/Zomato/ONDC, a packaging supplier, POS/CRM vendor, logistics partner, ingredient supplier, or marketing agency.

The target-account list uses real India QSR/operator names and public business context where available. The private outlet-level sales, inventory, menu, and health signals are simulated demo signals because those would only be real after connecting to the QSR company's authenticated POS, inventory, CRM, aggregator, loyalty, and review systems.

External signals are source-backed where possible. The app now stores official company pages, annual reports, stock-exchange filings, and official brand/store pages with source URLs and verification labels so the evidence can be opened and checked.

The QSR restaurant features are not used as a restaurant manager dashboard. They are used as meeting-prep intelligence. For the internal QSR login, sales trends, inventory risks, menu performance, outlet health, reviews, and competitor context help the representative prepare for partner, supplier, franchise, or leadership meetings. For the external partner login, those private operating signals are hidden and replaced with public/source-backed signals plus partner-specific alignment.

## How The App Works

1. The first screen is a login page with email and password only.
2. The app decides the role automatically from the credentials: internal QSR or external partner/vendor.
3. The internal login chooses the QSR company and meeting type. The external login chooses the target QSR account, their own company/entity, and entity type.
4. The rep enters their name and meeting objective.
5. The app loads structured account data from `data/company_signals.json`.
6. `modules/insight_agent.py` processes the account data through a role-specific India QSR intelligence model and creates:
   - opportunity score
   - risk score
   - meeting readiness score
   - model confidence
   - explainable reasons for the recommendation
   - account status
   - executive summary
   - likely pain points
   - account intelligence signals
   - talking points
   - discovery questions
   - recommended solution angles
7. Streamlit displays the output across separate pages.

Demo credentials:
- Internal QSR login: `internal.qsr@demo.com` / `qsr123`
- External partner login: `external.partner@demo.com` / `partner123`

## Pages And Features

### 1. Meeting Brief

This is the main page for quick pre-meeting preparation.

It shows:
- Company selected for the meeting
- Revenue growth and operating margin
- Account status, such as expansion-ready or growth with pressure
- AI-generated executive summary
- Recommended positioning
- Account intelligence signals
- Financial snapshot chart

The purpose is to help the representative understand the account and meeting context quickly. The internal version includes own-company operating signals. The external version stays public-only and partner-aligned.

### 2. Meeting Planner

This page turns the selected login context into a preparation checklist, agenda, value angle, and target decision. Internal users get partner, supplier, franchise, or leadership meeting preparation. External users get a partner/vendor preparation flow that avoids private QSR claims.

### 3. Account Signals

This page changes by login type.

For the internal QSR login, it includes:
- Sales trend: shows whether the account is growing or slowing down
- Inventory risk: shows possible stockout pressure across outlets
- Menu performance: shows which menu items are selling well and their margin
- Outlet health: shows which outlets may need attention
- Forecast, review theme, and competitor context

For the external partner login, it hides private operating data and shows:
- Public account signals
- Public digital signals
- Allowed evidence
- Hidden private data
- Partner-aligned discovery hypotheses

The purpose is to avoid the unrealistic assumption that an outside sales rep can see private restaurant inventory or outlet data.

### 4. External Signals

This page shows outside signals about the account.

It includes:
- News signals
- Social media and customer sentiment
- Primary trigger for the meeting
- Market momentum
- Rep takeaway

This helps the rep understand what recently happened around the account before the conversation.

### 5. Sales Playbook

This page turns role-specific insights into sales or partnership action.

It includes:
- Likely pain points
- Suggested talking points
- Meeting objective
- Recommended positioning
- Recommended solution angle
- Discovery questions
- Data boundary for the external partner login

This helps the rep move from research to actual meeting preparation.

### 6. Redacted Share Pack

This page creates a partner-safe summary by including public context, meeting focus, value angle, and approved wording while removing raw outlet sales, inventory levels, POS, loyalty, menu margin, and other sensitive data.

### 7. Permissioned Pilot Plan

This page builds a realistic pilot path with data needed, approvals, success metrics, and timeline. It makes external use credible because private data is only requested through consent and approval.

### 8. ROI Calculator

This page estimates impact using visible assumptions: baseline value, expected improvement, confidence adjustment, and pilot cost. It avoids fake precision by clearly showing that the result is a planning estimate.

### 9. Follow-Up Generator

This page drafts a role-safe follow-up email. Internal users get action-oriented partner follow-up. External users get a consent-safe pilot follow-up that avoids claiming private data access.

### 10. Stakeholders & Objections

This page maps likely stakeholders and gives responses to common objections around real data, AI trust, privacy, data sharing, and ROI.

### 11. Chatbot

This page lets the sales rep ask meeting-prep questions about the selected account.

It can answer:
- What is real and what is simulated?
- What proof links support the account information?
- What are the strongest external signals?
- What do the AI model scores mean?
- What should the sales rep say in the meeting?
- Which operating signals are only prototype/demo signals?
- How should the rep handle objections?
- Who should the rep speak to?
- What is the ROI/value story?
- What should the demo flow be?
- What follow-up email should the rep send?

The chatbot is cost-aware. It first analyzes the question and decides whether the answer can be handled locally, needs the LLM, or needs LLM + live web search.

Local answers are used for greetings, simple meanings, calculations, stored source links, model score summaries, brief summaries, and data-boundary questions. This avoids wasting API tokens on questions the app can answer from its own data.

LLM-only answers are used for deeper custom writing, pitch wording, customer-specific explanation, and synthesis that does not require current web verification.

LLM + web search is used only when the user asks for latest/current/recent context, online verification, search, or updated public evidence. In that route, the selected account context, model output, source links, recent chat context, login type, data-access boundary, entity alignment, and response preferences are sent to the OpenAI LLM with the web-search tool enabled.

For the external partner login, the chatbot prompt explicitly tells the LLM not to use or imply access to private outlet sales, inventory, menu margin, POS, loyalty, or outlet-health data.

It can adapt the answer for different audiences such as a sales representative, customer executive, operations head, finance team, technical team, or beginner student. It can also change the answer style into simple wording, balanced business wording, deep technical wording, step-by-step explanation, meeting-ready answer, calculation-focused answer, or detailed analysis with sources.

If the OpenAI API key is missing, local chatbot answers still work. Questions that need LLM or web search clearly tell the user to configure `OPENAI_API_KEY`.

## Technical Implementation

The app is built using Streamlit.

Important files:
- `app.py`: Creates the multipage navigation.
- `views/meeting_brief.py`: Displays the meeting brief and financial snapshot.
- `views/meeting_planner.py`: Displays the role-specific meeting checklist, agenda, and target decision.
- `views/account_signals.py`: Displays QSR account operating signals.
- `views/external_signals.py`: Displays news and social signals.
- `views/sales_playbook.py`: Displays sales-ready talking points and questions.
- `views/share_pack.py`: Displays the redacted partner-safe share pack.
- `views/pilot_plan.py`: Displays the permissioned pilot plan.
- `views/roi_calculator.py`: Displays the ROI and impact calculator.
- `views/follow_up.py`: Displays the follow-up email generator.
- `views/stakeholders.py`: Displays stakeholder map and objection handler.
- `views/chatbot.py`: Displays the LLM chatbot controls and chat interface.
- `modules/role_features.py`: Contains the role-aware high-credibility feature logic.
- `modules/user_modes.py`: Defines the two demo logins, role permissions, internal meeting types, and external partner/entity alignment.
- `modules/insight_agent.py`: Contains the logic that converts account data into insights.
- `modules/llm_chatbot.py`: Builds the selected-account context, local answer router, calculation responses, chatbot prompts, LLM-only calls, LLM + web-search calls, and source extraction.
- `modules/ui.py`: Contains shared UI functions for sidebar, headers, and cards.
- `data/company_signals.json`: Contains sample account data used by the app.

## Why This Matches The Problem Statement

The original problem statement is about helping sales representatives reduce manual research before meetings. This app directly supports that by giving the representative one place to see company context, financial signals, news, social sentiment, role-appropriate account signals, and a meeting playbook.

The two-login design fixes the privacy issue around internal QSR data. Internal QSR users can use their own operating signals. External partner/vendor users only see public and permissioned context, with a pitch aligned to their own entity type.

## Demo Script

Start on the login page. Enter the internal QSR credentials and show how operating signals support a supplier, aggregator, franchise, or leadership meeting. Then log out and enter the external partner credentials. Choose an entity type such as packaging supplier or aggregator platform and show how the same pages become public-only and partner-aligned. Finish on Chatbot and ask it to explain what private data the external rep should avoid mentioning, or ask it to build a partner-specific pitch using app data plus live web search.
