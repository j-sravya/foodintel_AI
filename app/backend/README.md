# Backend API And AI Agent Layer

This folder is the target backend for the production version.

Recommended stack:

```text
FastAPI
Supabase Python client
OpenAI / LLM client
python-docx for pitch documents
Stripe SDK
PostHog server events
```

## API Responsibilities

- Authenticate requests through Supabase JWT.
- Load seller category and product catalog.
- Load active prospect and meeting context.
- Retrieve signals from Supabase.
- Run AI agent workflow.
- Generate prospect brief, pitch, questions, objections and follow-up.
- Store brief versions and audit logs.

## Agent Workflow

```text
Meeting Detection Agent
Research Agent
Signal Orchestration Agent
Review Analysis Agent
Competitor Intelligence Agent
Insight Ranking Agent
Sales Strategy And Follow-up Agent
```

