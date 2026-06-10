# FoodIntel AI Production-Ready Duplicate

This folder is a lean duplicate of the current FoodIntel AI Streamlit MVP, prepared for a future production architecture.

## Current MVP

The existing Streamlit app is still available:

```bash
streamlit run app.py
```

It uses:

- `app.py`
- `views/`
- `modules/`
- `data/`
- `assets/`

## New Target Architecture

```text
React frontend
↓
Supabase Auth
↓
FastAPI / AI backend
↓
Supabase Postgres
↓
Agentic RAG intelligence layer
↓
PostHog analytics
↓
Stripe billing
```

## Folder Map

| Folder | Purpose |
|---|---|
| `frontend/` | Working React UI to build/run in Antigravity |
| `backend/` | Working FastAPI API and AI intelligence services |
| `supabase/` | Database schema and authentication plan |
| `analytics/` | PostHog event tracking plan |
| `billing/` | Stripe subscription model |
| `docs/architecture/` | Production architecture and migration roadmap |
| `views/`, `modules/`, `data/` | Current working Streamlit MVP |

## Best Development Path

1. Keep Streamlit as the working academic demo.
2. Run the new FastAPI backend from `backend/`.
3. Run the new React frontend from `frontend/`.
4. Use `supabase/migrations/001_initial_schema.sql` to create the production database when you are ready.
5. Connect Supabase, PostHog and Stripe keys through `.env` files.

See `RUN_PRODUCTION_APP.md` for commands.

## Important

This duplicate does not replace the original project at:

```text
/Users/sravyajayaram/Desktop/bitsom/project
```

All architecture changes here are isolated in:

```text
/Users/sravyajayaram/Desktop/foodintel-ai-production-lean
```
