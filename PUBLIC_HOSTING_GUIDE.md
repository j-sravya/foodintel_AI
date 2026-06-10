# Public Hosting Guide - FoodIntel AI

This app has two parts:

```text
React frontend  -> public website
Python backend  -> public API
Supabase        -> hosted database/auth layer
PostHog         -> hosted analytics
Stripe          -> demo/payment layer
```

## Recommended Hosting Setup

Use:

- **Backend API:** Render or Railway
- **Frontend website:** Vercel
- **Database/auth:** Supabase
- **Analytics:** PostHog

This is better than trying to host everything on one static site because the app needs a Python API for intelligence routes such as `/brief`, `/copilot`, `/command-center` and `/followup`.

---

## Step 1: Put This Folder On GitHub

Create a GitHub repository and upload this clean folder.

Recommended repository name:

```text
foodintel-ai-final
```

Keep this structure:

```text
FoodIntel_AI_Final_Clean/
├── app/backend
├── app/frontend
├── app/data
├── app/supabase
├── submission
└── wireframes
```

Do not upload real `.env` files or secrets.

---

## Step 2: Deploy Backend API

Use Render/Railway-style Python web service hosting.

Backend settings:

```text
Root directory: app/backend
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Environment variables:

```text
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
POSTHOG_KEY=your_posthog_project_key
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
```

After deployment, test:

```text
https://your-backend-url/health
```

Expected result:

```json
{
  "status": "ok",
  "service": "FoodIntel AI production backend"
}
```

---

## Step 3: Deploy Frontend Website

Use Vercel.

Frontend settings:

```text
Root directory: app/frontend
Build command: npm run build
Output directory: dist
```

Environment variables:

```text
VITE_API_BASE_URL=https://your-backend-url
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_POSTHOG_KEY=your_posthog_project_key
VITE_STRIPE_PUBLISHABLE_KEY=
```

Important:

```text
VITE_API_BASE_URL must be the public backend URL, not localhost.
```

---

## Step 4: Test Public App

Open the public frontend URL and test:

1. Login with:

```text
Username: packaging.rep@foodintel.ai
Password: packaging123
```

2. Check Command Center loads meetings.
3. Open Prospect Brief.
4. Ask AI Copilot:

```text
How should I pitch leak-proof packaging and compare competitors?
```

5. Confirm the Copilot answer shows:

```text
Answer
From Database
From Internet / Proxy Signals
Recommendation
Sources
```

---

## Production Note For Submission

The hosted MVP uses structured backend data and proxy web signals. The architecture is production-ready for live connectors such as financial APIs, news APIs, LinkedIn, Instagram, Google Reviews, food delivery platforms and CRM systems.
