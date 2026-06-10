# FoodIntel AI Production Architecture

FoodIntel AI can move from the current Streamlit MVP into a production SaaS architecture with a React frontend, Supabase backend, AI agent service, PostHog analytics, and Stripe billing.

## Target Stack

| Layer | Tool | Purpose |
|---|---|---|
| Frontend UI | React, built in Antigravity | Premium SaaS interface, page routing, global context bar, category login, prospect brief, pitch downloads |
| Backend API | FastAPI or server functions | Business logic, AI agent orchestration, pitch generation, secure data access |
| Database | Supabase Postgres | Users, seller categories, prospects, meetings, signals, insights, CRM memory, brief versions |
| Authentication | Supabase Auth | Company login, sales category access, user sessions, role-based access |
| AI Agent Layer | Python services / LLM APIs | Research agent, signal agent, review agent, competitor agent, insight ranking, strategy, follow-up |
| Analytics | PostHog | Track user behavior, page usage, brief views, pitch downloads, follow-up generation |
| Payments | Stripe | SaaS subscription plans, billing, team seats, enterprise upgrades |
| External Data | APIs and connectors | News, financial data, LinkedIn, Instagram, Google Reviews, CRM, delivery platforms |

## High-Level Flow

```text
React Frontend
↓
Supabase Auth
↓
FastAPI / AI Backend
↓
Supabase Postgres + Evidence Store
↓
Agentic RAG Intelligence Layer
↓
PostHog Analytics + Stripe Billing
```

## User Workflow

```text
Login by company and sales category
↓
Select active prospect / meeting
↓
AI agents retrieve prospect, product, signal, competitor and CRM memory
↓
Insight ranking engine generates trusted meeting brief
↓
Sales rep downloads pitch and prepares questions
↓
Follow-up Studio creates email, CRM note and next action
↓
PostHog tracks workflow usage and Stripe manages plan access
```

## Why This Architecture Is Better

- React gives the app a polished enterprise SaaS experience.
- Supabase solves backend data, authentication, and row-level security quickly.
- FastAPI keeps AI agent logic separate from UI.
- PostHog proves product value with usage analytics.
- Stripe supports the SaaS business model.
- The current Streamlit MVP can remain as a prototype while the React/Supabase version becomes the production path.

