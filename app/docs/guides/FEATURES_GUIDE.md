# QSR AccountBrief AI - Features Guide

This file explains every feature in the project from the basics. It is written for someone who is seeing the app for the first time and wants to understand what each feature does, why it exists, and how it works.

## 1. Basic Idea Of The Project

The project is called **QSR AccountBrief AI**.

It is an AI-powered pre-meeting preparation app for sales and partnership representatives in the QSR and restaurant industry.

The original problem statement says that sales representatives need timely company insights from financial data, news, and social media before meetings. This app applies that problem to the India QSR industry.

In simple words:

- A sales representative has a meeting.
- Before the meeting, they need to understand the company.
- Normally they search websites, annual reports, news, social media, reviews, and internal notes manually.
- This app collects and organizes that information into a meeting-ready brief.
- It also explains what the rep can safely say, what data is private, what questions to ask, and what next step to propose.

## 2. Two User Types

The app has two different user flows.

### Internal QSR Representative

This user works inside the restaurant or QSR company.

Example:

- A Domino's India internal team member preparing for a supplier meeting.
- A QSR operations or partnership person preparing for a Zomato or Swiggy discussion.
- A regional team preparing for a franchise or leadership review.

This user can see internal-style operating signals in the prototype, such as:

- sales trend
- inventory risk
- menu performance
- outlet health
- demand forecast

Important: in the current app, these internal operating signals are simulated demo data. In a real company, they would come from POS, inventory, CRM, aggregator, loyalty, and operations systems.

### External Partner Or Vendor Representative

This user is outside the QSR company.

Example:

- Swiggy or Zomato representative
- packaging supplier
- POS or CRM vendor
- logistics partner
- ingredient supplier
- marketing or loyalty agency

This user cannot see private QSR operating data.

They only see:

- public company information
- official source links
- public news and digital signals
- public customer or review themes
- permissioned pilot suggestions

This makes the app realistic because an outside sales rep should not have private outlet-level inventory, POS, loyalty, margin, or sales data unless the QSR gives permission.

## 3. Login Feature

### What It Does

The login page is the first screen of the app.

It asks for:

- email
- password

The app automatically decides whether the user is internal or external based on the credentials.

### Demo Credentials

Internal QSR login:

```text
internal.qsr@demo.com
qsr123
```

External partner login:

```text
external.partner@demo.com
partner123
```

### How It Works

The login credentials are defined in:

```text
modules/user_modes.py
```

The login UI is rendered from:

```text
modules/ui.py
views/login.py
```

When the user logs in successfully, the app stores the active login in Streamlit session state. After that, the multipage app becomes available.

## 4. Sidebar Context Feature

### What It Does

After login, the sidebar lets the user select the meeting context.

For an internal QSR user, the sidebar asks for:

- QSR company
- representative name
- meeting type
- meeting objective

For an external partner user, the sidebar asks for:

- target India QSR account
- representative name
- user's company/entity
- user's entity type
- meeting objective

### Why It Matters

The app output changes based on this context.

For example:

- A packaging supplier should not get the same pitch as a delivery aggregator.
- An internal leadership review should not look the same as an external partner pitch.

### How It Works

The sidebar is built in:

```text
modules/ui.py
```

The internal and external alignment rules are stored in:

```text
modules/user_modes.py
```

## 5. Meeting Brief Page

### What It Does

The Meeting Brief page is the main pre-meeting summary.

It shows:

- selected company
- revenue growth
- operating margin
- account status
- executive summary
- recommended positioning
- recommendation reasoning
- account intelligence signals
- financial snapshot
- real-vs-demo data labels
- source proof table
- downloadable meeting brief

### How It Helps

This page helps the sales rep quickly understand:

- what the account is about
- whether the account is growing or under pressure
- what angle to use in the meeting
- what signals are important before speaking to the customer
- why the recommendation was made
- what data is public, simulated, or permissioned
- what source proof can be cited in the meeting

### How It Works

The page uses account data from:

```text
data/company_signals.json
```

The insight logic is in:

```text
modules/insight_agent.py
```

The page file is:

```text
views/meeting_brief.py
```

## 6. Meeting Planner Page

### What It Does

The Meeting Planner page creates a role-specific meeting plan.

It shows:

- meeting focus
- value angle
- target decision
- preparation checklist
- meeting agenda

### Internal Example

If the user selects a supplier or packaging meeting, the planner focuses on:

- stockout risk
- replenishment
- service levels
- supply consistency

### External Example

If the user is a packaging supplier, the planner focuses on:

- public expansion context
- delivery packaging needs
- permissioned pilot proposal
- questions instead of private claims

### How It Works

The logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/meeting_planner.py
```

## 7. Account Signals Page

### What It Does

The Account Signals page changes based on the login type.

### Internal User View

Internal users can see simulated internal operating signals:

- sales trend
- inventory risk
- menu performance
- outlet health
- forecast
- review theme
- competitor context

These signals help internal QSR teams prepare for supplier, aggregator, franchise, or leadership meetings.

### External User View

External users do not see private operating signals.

Instead, they see:

- public account signals
- public digital signals
- allowed evidence
- hidden private data
- partner-aligned hypotheses

### How It Works

The page checks the current user role.

If the user is internal, it displays internal-style demo operating data.

If the user is external, it hides private data and shows public-only context.

The page file is:

```text
views/account_signals.py
```

The data helper functions are in:

```text
modules/insight_agent.py
```

## 8. External Signals Page

### What It Does

The External Signals page shows outside signals about the selected QSR account.

It includes:

- news signals
- social or public customer sentiment
- primary meeting trigger
- market momentum
- public source links
- source proof cards
- claim supported
- source type
- last checked date
- meeting use for each claim

### How It Helps

This page helps the rep understand what is happening around the company before the meeting.

Example:

- expansion news
- annual report updates
- public brand or investor pages
- public customer sentiment themes
- source-backed claims that can be cited safely

### How It Works

The source links are stored in:

```text
data/company_signals.json
```

The page file is:

```text
views/external_signals.py
```

## 9. Sales Playbook Page

### What It Does

The Sales Playbook page converts the account brief into meeting actions.

It shows:

- likely pain points
- suggested talking points
- meeting objective
- recommended positioning
- recommended solution angle
- discovery questions
- data boundary reminder for external users

### How It Helps

The rep does not only read information. They get help with what to say and what to ask.

Example:

- "Which delivery regions are most important for growth?"
- "What data can be safely shared for a pilot?"
- "Which operating issue should be solved first?"

### How It Works

The talking points and questions are generated in:

```text
modules/insight_agent.py
```

The page file is:

```text
views/sales_playbook.py
```

## 10. Share Pack Page

### What It Does

The Share Pack page creates a safe summary that can be shared with a partner or stakeholder.

It includes:

- what is included in the safe pack
- what is removed or redacted
- safe language to use
- safe to say / ask permission first / do not say rules
- customer-friendly wording
- partner-safe summary
- download button for the safe share pack

### Why It Matters

Internal analysis may contain sensitive information.

The Share Pack helps convert internal thinking into external-safe wording.

It removes:

- raw outlet sales
- raw inventory levels
- menu margin by outlet
- POS data
- loyalty data
- customer-level data
- internal commercial terms

It also shows exactly how the rep should phrase the boundary without sounding defensive.

### How It Works

The redaction logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/share_pack.py
```

## 11. Pilot Plan Page

### What It Does

The Pilot Plan page builds a realistic next step after the meeting.

It shows:

- pilot scope
- data needed
- approvals required
- success metrics
- timeline
- evidence needed for the recommendation

### Why It Matters

In the real world, a customer will not simply hand over private data.

They may agree to a small permissioned pilot if:

- the problem is important
- the data needed is clear
- the approvals are clear
- the success metric is clear
- the evidence needed to prove value is clear

### How It Works

For external users, the pilot plan asks for customer-approved data only.

For internal users, it focuses on internal action planning with approved stakeholders.

The page also lists the evidence needed before a recommendation can become a real production pilot.

The logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/pilot_plan.py
```

## 12. ROI Calculator Page

### What It Does

The ROI Calculator estimates possible business impact.

It asks for:

- baseline value
- expected improvement percentage
- confidence adjustment
- pilot or implementation cost

It calculates:

- gross monthly benefit
- confidence-adjusted benefit
- net benefit after pilot cost
- estimated ROI percentage

### Basic Formula

Gross benefit:

```text
baseline value x expected improvement %
```

Confidence-adjusted benefit:

```text
gross benefit x confidence %
```

Net benefit:

```text
confidence-adjusted benefit - pilot cost
```

ROI:

```text
net benefit / pilot cost x 100
```

### Why It Matters

Sales reps often need to explain why a customer should spend time or money on a pilot.

This page gives a simple planning estimate. It is not a final financial guarantee.

### How It Works

The calculation logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/roi_calculator.py
```

## 13. Follow-Up Page

### What It Does

The Follow-Up page generates a role-safe follow-up email after the meeting.

It asks for:

- recipient name
- agreed next step

Then it creates:

- subject line
- email draft

### Internal User Version

The internal version focuses on internal or partner action planning.

### External User Version

The external version avoids claiming access to private data and suggests a permissioned pilot.

### How It Works

The email template logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/follow_up.py
```

## 14. Stakeholders Page

### What It Does

The Stakeholders page helps identify who should be involved in the meeting process.

It includes:

- suggested stakeholder map
- objection handler

### Stakeholder Examples

For external users:

- business owner
- data owner or IT
- finance or procurement
- user champion

For internal users:

- internal owner
- data owner
- partner stakeholder
- finance or leadership

### Objection Examples

The page helps answer questions like:

- Is this data real?
- Can we trust the AI score?
- What about privacy?
- Why should we share data?
- Can we show this to a partner?

### How It Works

The stakeholder and objection logic is in:

```text
modules/role_features.py
```

The page file is:

```text
views/stakeholders.py
```

## 15. Chatbot Page

### What It Does

The Chatbot page lets the sales rep ask questions about the selected account and meeting context.

Example questions:

- What should I say in the meeting?
- Tell me about the inventory risk.
- What does operating margin mean?
- What proof links can I cite?
- What private data should I avoid?
- Build a pitch for a packaging supplier.
- Use latest web context for this company.

### How The Chatbot Saves API Cost

The chatbot first analyzes the question.

Then it decides the cheapest safe route:

1. Local answer
2. LLM-only answer
3. LLM plus web search

### Local Answer

Used for:

- greetings
- simple meanings
- calculations
- stored account signals
- source links already in the app
- data-boundary questions
- model-score explanations
- source proof
- real-vs-demo data labels

This does not need the OpenAI API.

### LLM-Only Answer

Used for:

- deeper custom wording
- pitch writing
- synthesis
- audience-specific explanation
- customer-specific wording and structure

This needs `OPENAI_API_KEY`.

### LLM Plus Web Search

Used only when the question asks for:

- latest information
- current news
- online verification
- search
- recent public evidence

This also needs `OPENAI_API_KEY`.

### Why It Matters

Earlier, the chatbot used the API even for small questions like "hey". That wastes tokens and can hit quota errors.

Now the chatbot also shows answer quality checks: app-data grounding, audience fit, private-data warning, and web-search restraint.

Now the chatbot routes simple questions locally first.

### How It Works

The chatbot logic is in:

```text
modules/llm_chatbot.py
```

The chatbot page is:

```text
views/chatbot.py
```

## 16. Public Source Evidence Feature

### What It Does

The app stores public source links for each QSR account.

These include:

- official company pages
- annual reports
- investor pages
- brand pages
- public filings or official documents

### Why It Matters

The user asked whether the data is real or fake.

This feature helps separate:

- real public data
- simulated demo internal data
- permissioned data that would exist only in real production

### How It Works

The public links are stored in:

```text
data/company_signals.json
```

They are displayed in:

```text
views/external_signals.py
```

## 17. Internal Operating Signals Feature

### What It Does

The app includes restaurant-style operating signals:

- sales trend
- inventory risk
- menu performance
- outlet health
- demand forecast
- competitor context

### Important Data Note

These signals are simulated in the prototype.

They are not real private data from the listed QSR companies.

In a real deployment, these would come only from approved internal systems such as:

- POS
- inventory software
- CRM
- loyalty system
- aggregator dashboard
- operations dashboard

### Why It Still Matters

The feature is realistic for an internal QSR user.

It is not realistic for an external sales rep unless the QSR approves a pilot or data-sharing agreement.

That is why the app hides these signals from external users.

## 18. Role-Based Data Boundary Feature

### What It Does

This feature controls what each user type can see.

Internal QSR user:

- can see simulated internal signals
- can prepare for internal or partner meetings
- still gets warnings about what not to share externally

External partner user:

- cannot see private operating signals
- sees public and permissioned data only
- gets safe discovery questions and pilot language

### Why It Matters

This is one of the most important real-world corrections in the project.

It makes the app more credible because private restaurant data should not be available to outsiders without permission.

### How It Works

Role logic is mostly defined in:

```text
modules/user_modes.py
modules/ui.py
modules/role_features.py
modules/insight_agent.py
```

## 19. India-First QSR Account List

### What It Does

The app lets users select from India-relevant QSR or restaurant operator accounts.

Current accounts include:

- Jubilant FoodWorks - Domino's India
- Westlife Foodworld - McDonald's India West & South
- Devyani International - KFC, Pizza Hut, Costa Coffee
- Restaurant Brands Asia - Burger King India
- Sapphire Foods India - KFC and Pizza Hut
- Barbeque-Nation Hospitality
- Wow! Momo Foods

### How It Works

The account data is stored in:

```text
data/company_signals.json
```

The sidebar loads these account names through:

```text
modules/insight_agent.py
modules/ui.py
```

## 20. Colab Notebook Feature

### What It Does

The project includes a notebook:

```text
Untitled25.ipynb
```

This notebook writes the app files into a Colab runtime and runs the Streamlit app.

### Why It Exists

The user asked whether the project can be built or run in Google Colab.

The notebook is a Colab-friendly version of the project.

### How It Works

The notebook contains cells that:

- install requirements
- create project folders
- write data files
- write module files
- write view files
- run Streamlit

## 21. Submission Document Features

### What It Does

The project folder includes Word submission files:

```text
QSR AccountBrief AI - Phase by Phase Submission.docx
QSR AccountBrief AI - Full Project Submission.docx
```

### Why They Exist

The user asked for submission documents based on the project guidelines.

The phase-by-phase document follows the guideline order more directly.

### What They Include

- team list section
- Phase 1 answers
- Phase 2 answers
- Phase 3 answers
- Phase 4A answers
- Phase 4B answers
- Phase 5 answers
- PRD
- MVP details
- placeholders for required real evidence

## 22. How The App Runs

From the `project` folder:

```bash
cd /Users/sravyajayaram/Desktop/bitsom/project
../.venv/bin/python -m streamlit run app.py
```

Then open the URL shown in the terminal.

Usually it is:

```text
http://localhost:8501
```

or:

```text
http://127.0.0.1:8501
```

## 23. How The Files Are Organized

Main app entry:

```text
app.py
```

Pages:

```text
views/
```

Shared app logic:

```text
modules/
```

Account data:

```text
data/company_signals.json
```

Images and walkthrough assets:

```text
assets/
```

Submission documents:

```text
QSR AccountBrief AI - Phase by Phase Submission.docx
QSR AccountBrief AI - Full Project Submission.docx
```

Colab notebook:

```text
Untitled25.ipynb
```

## 24. What Is Real And What Is Simulated

### Real Or Source-Backed

- company names
- official source links
- public source types
- annual report links where included
- app structure
- role-based logic
- chatbot routing logic
- ROI formula
- generated documents

### Simulated Demo Data

- internal outlet-level sales
- inventory risk
- menu margin
- outlet health
- internal demand forecast
- some social/review theme summaries

### Permissioned In Real Deployment

These would require QSR approval:

- POS data
- inventory data
- loyalty data
- customer-level data
- aggregator dashboard data
- outlet-level performance data
- menu margin data

## 25. Most Important Project Logic In One Line

The app prepares sales representatives for QSR meetings by combining public evidence, role-safe account signals, AI-generated recommendations, and a chatbot, while making sure external users do not see private restaurant data.
