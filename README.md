# FoodIntel AI - Final Clean Project Folder

This is the single clean folder for the FoodIntel AI BITSoM PM capstone submission.

## Folder Structure

```text
FoodIntel_AI_Final_Clean/
├── app/
│   ├── backend/          # Python backend API and AI intelligence logic
│   ├── frontend/         # React + Vite frontend app
│   ├── data/             # Food industry prospect and signal datasets
│   ├── supabase/         # Supabase schema and seed files
│   ├── assets/           # Architecture, canvas, walkthrough and evidence images
│   ├── analytics/        # PostHog event documentation
│   ├── billing/          # Stripe pricing documentation
│   └── docs/             # Architecture, setup and guide documents
├── submission/
│   ├── FoodIntel AI - Final Submission Deck - Updated RAG Copilot.pptx
│   ├── FoodIntel AI - Final Project Documentation.docx
│   └── FINAL_PROJECT_DOCUMENTATION.md
└── wireframes/
    ├── 01-login.svg
    ├── 02-command-center.svg
    ├── 03-prospect-brief.svg
    ├── 04-ai-copilot.svg
    ├── 05-ai-workflow.svg
    ├── 06-follow-up-studio.svg
    └── index.html
```

## What To Submit

Use these final submission files:

- `submission/FoodIntel AI - Final Submission Deck - Updated RAG Copilot.pptx`
- `submission/FoodIntel AI - Final Project Documentation.docx`
- `wireframes/` for Figma-ready wireframe evidence
- App demo recording link, if required by LMS

## How To Run The App

Open two terminals.

### Terminal 1: Backend

```bash
cd app/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python simple_api.py
```

Backend health check:

```text
http://localhost:8787/health
```

### Terminal 2: Frontend

```bash
cd app/frontend
npm install
npm run dev -- --host 0.0.0.0
```

Open:

```text
http://localhost:5173/
```

## Demo Login

```text
Username: packaging.rep@foodintel.ai
Password: packaging123
```

Other available categories are documented in the app backend.

## Notes

- Real `.env` files and secrets are not included in this clean folder.
- `node_modules`, build outputs, caches, temporary Word lock files and old app versions are excluded.
- The current app includes the updated RAG + web/proxy-signal AI Copilot flow.
