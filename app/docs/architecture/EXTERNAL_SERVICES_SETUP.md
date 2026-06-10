# External Services Setup

This guide connects the production-style FoodIntel AI app to Supabase, PostHog, Stripe and Antigravity.

## 1. Antigravity

Use Antigravity as the frontend coding workspace.

Open this folder:

```text
/Users/sravyajayaram/Desktop/foodintel-ai-production-lean
```

Main frontend files:

```text
frontend/src/main.jsx
frontend/src/styles.css
frontend/src/api.js
frontend/src/integrations.js
```

Run frontend:

```bash
cd frontend
npm install
npm run dev
```

## 2. Supabase

Use Supabase for database, authentication and future row-level security.

### Create Project

1. Go to Supabase.
2. Create a new project named `foodintel-ai`.
3. Open SQL Editor.
4. Paste and run:

```text
supabase/migrations/001_initial_schema.sql
```

### Add Environment Keys

Create this file:

```text
/Users/sravyajayaram/Desktop/foodintel-ai-production-lean/.env
```

Add:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```

Create this file:

```text
/Users/sravyajayaram/Desktop/foodintel-ai-production-lean/frontend/.env
```

Add:

```env
VITE_API_BASE_URL=http://localhost:8787
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### What Supabase Will Store

- Companies
- Sales category users
- Products
- Prospects
- Meetings
- Source registry
- Raw signals
- Insight audit logs
- Product match scores
- Competitor mentions
- Account history
- Brief versions
- Follow-up actions

## 3. PostHog

Use PostHog for user behavior analytics.

### Events Already Planned

- `category_login_completed`
- `prospect_selected`
- `brief_generated`
- `pitch_downloaded`
- `followup_generated`
- `copilot_question_asked`
- `subscription_checkout_started`

### Add Keys

In root `.env`:

```env
POSTHOG_KEY=your_posthog_project_api_key
```

In `frontend/.env`:

```env
VITE_POSTHOG_KEY=your_posthog_project_api_key
```

When keys are missing, the app remains in demo mode.

## 4. Stripe

Use Stripe for subscriptions and SaaS billing.

### Create Products

Create three subscription prices:

```text
Starter
Growth
Enterprise
```

Copy the Stripe Price IDs.

### Add Keys

In root `.env`:

```env
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
STRIPE_PRICE_STARTER=price_xxx
STRIPE_PRICE_GROWTH=price_xxx
STRIPE_PRICE_ENTERPRISE=price_xxx
STRIPE_SUCCESS_URL=http://localhost:5173?checkout=success
STRIPE_CANCEL_URL=http://localhost:5173?checkout=cancelled
```

In `frontend/.env`:

```env
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key
```

When Stripe keys are missing, the Billing page shows demo checkout mode.

## 5. Run Full App

Terminal 1:

```bash
cd /Users/sravyajayaram/Desktop/foodintel-ai-production-lean/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_api.py
```

Terminal 2:

```bash
cd /Users/sravyajayaram/Desktop/foodintel-ai-production-lean/frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

## 6. Demo Mode vs Production Mode

| Service | Demo Mode | Production Mode |
|---|---|---|
| Supabase | Local JSON data | Auth + Postgres database |
| PostHog | Events accepted locally | Events sent to PostHog |
| Stripe | Demo checkout alert | Stripe Checkout redirect |
| Antigravity | Optional editor | Frontend development workspace |

