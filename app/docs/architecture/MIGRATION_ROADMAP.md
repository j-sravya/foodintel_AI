# Migration Roadmap

## Phase 1: Keep Current MVP Stable

- Keep the Streamlit app working as the demo MVP.
- Preserve existing datasets, prospect logic, category login, pitch downloads and AI workflow pages.
- Use the existing app as the reference for React screens.

## Phase 2: Supabase Foundation

- Create Supabase project.
- Add tables for users, seller categories, product catalog, prospects, meetings, signals, insights, CRM history, follow-ups and pitch documents.
- Enable Supabase Auth.
- Add row-level security for company-specific data.

## Phase 3: React Frontend

- Build React layout in Antigravity.
- Implement login, global context bar, Command Center, Prospect Brief, Opportunity Radar, CRM Timeline, Follow-up Studio, AI Copilot and AI Workflow.
- Connect screens to Supabase read APIs first.

## Phase 4: AI Backend

- Move intelligence logic from Streamlit modules into FastAPI services.
- Add API routes for meeting briefs, product matches, pitch generation, follow-up drafts and copilot answers.
- Keep trust data mandatory: source, timestamp, confidence and why this matters.

## Phase 5: Analytics And Billing

- Add PostHog event tracking for key actions.
- Add Stripe subscription plans.
- Use plan limits for briefs generated, team seats, pitch downloads and CRM integrations.

## Phase 6: Production Data Integrations

- Connect live news, financial, review, social and CRM APIs.
- Replace proxy signals with real-time data where available.
- Keep the Evidence & Audit Intelligence Store for explainability.

