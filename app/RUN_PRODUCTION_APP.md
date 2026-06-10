# Run The New Production-Style App

This duplicate contains two runnable apps:

1. Current Streamlit MVP
2. New React + FastAPI production-style app

## 1. Run Backend API

From the duplicate folder:

```bash
cd /Users/sravyajayaram/Desktop/foodintel-ai-production-lean/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_api.py
```

Backend URL:

```text
http://localhost:8787
```

Health check:

```text
http://localhost:8787/health
```

## 2. Run React Frontend

Open a second terminal:

```bash
cd /Users/sravyajayaram/Desktop/foodintel-ai-production-lean/frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Demo Login

```text
packaging.rep@foodintel.ai / packaging123
ingredients.rep@foodintel.ai / ingredients123
bakery.rep@foodintel.ai / bakery123
beverages.rep@foodintel.ai / beverages123
hygiene.rep@foodintel.ai / hygiene123
equipment.rep@foodintel.ai / equipment123
crm.rep@foodintel.ai / crm123
logistics.rep@foodintel.ai / logistics123
```

## What This New App Includes

- React SaaS frontend
- FastAPI backend
- Category login
- Global context bar
- Command Center
- Prospect Brief
- Opportunity Radar
- CRM Timeline
- Follow-up Studio
- AI Copilot
- AI Workflow
- Billing screen
- Supabase schema
- PostHog event plan and frontend hooks
- Stripe billing plan and checkout-ready structure

## Important

The current project is still safe here:

```text
/Users/sravyajayaram/Desktop/bitsom/project
```

This new production-style version is here:

```text
/Users/sravyajayaram/Desktop/foodintel-ai-production-lean
```

## Connect External Services

Use this guide:

```text
docs/architecture/EXTERNAL_SERVICES_SETUP.md
```

The app runs without external keys in demo mode. Add Supabase, PostHog and Stripe keys when you want production mode.
