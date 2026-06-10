# Backend Data Model

This app uses a structured backend store for the food-industry sales intelligence workflow. The generated backend file is:

`data/sales_intelligence_backend.json`

It is produced by:

`modules/backend_store.py`

## Core Context

`active_context` is the single context object every page should respect.

It stores:

- `seller_category`
- `seller_company`
- `product_catalog`
- `active_prospect_id`
- `active_meeting_id`
- `active_area`

This prevents the app from showing one prospect/category on one page and a different prospect/category on another page.

## Backend Objects

| Object | Purpose |
| --- | --- |
| `meetings` | Real scheduled meeting records by category, rep, prospect, time, stage, goal, attendees, decision maker, and last meeting date. |
| `source_registry` | Source metadata for every prospect signal, including financial proxy, news/public listing, social/review proxy, and product-catalog source. |
| `raw_signals` | Raw signal layer before AI summarization, with topic, sentiment, relevance score, and source type. |
| `insight_audit_log` | Explainable AI layer: what insight was generated, which sources supported it, which agent created it, and confidence score. |
| `product_match_scores` | Stored product-to-prospect match logic for the logged-in sales category. |
| `competitor_mentions` | Category-specific competitor and supplier alternatives to verify during the meeting. |
| `account_history` | Relationship memory and “what changed since last meeting” events. |
| `rep_actions` | AI-generated workflow tasks such as review brief, download pitch, verify supplier, and send follow-up. |
| `brief_versions` | Version history of generated meeting briefs before the meeting. |
| `impact_metrics` | Time saved, briefs generated, meetings prepared, follow-ups generated, and manual research reduction. |

## 8-Layer App Architecture

| Layer | Purpose |
| --- | --- |
| Data Layer | Stores prospects, restaurant data, product catalog, meeting records, source records, raw signals, competitors, and impact metrics. |
| Context Layer | Keeps the logged-in seller category, seller company, active prospect, active meeting, active area, and product focus consistent across all pages. |
| Signal Orchestration Layer | Collects and ranks financial, news, social, review, and competitor signals before AI generates insights. |
| AI Intelligence Layer | Converts signals into pain points, lead scores, opportunity scores, product matches, meeting briefs, questions, objection handling, and pitches. |
| Memory Layer | Stores previous meetings, objections, follow-ups, CRM history, brief versions, and what changed since last meeting. |
| Trust & Explainability Layer | Shows source, timestamp, confidence score, raw evidence, agent name, and why each insight matters. |
| Workflow Automation Layer | Turns intelligence into pitch downloads, CRM actions, follow-up drafts, reminders, and rep tasks. |
| Frontend Experience Layer | Presents Seller Setup, Command Center, Prospect Brief, Opportunity Radar, CRM Timeline, Follow-up Studio, AI Copilot, and AI Workflow. |

## Why This Fits The Problem Statement

The problem asks for an AI-powered agent that curates timely, contextual company insights from financial data, news, and social media before meetings.

This backend supports that by storing:

- the meeting that triggered the agent workflow,
- the prospect and seller category context,
- source-backed signals,
- raw evidence before summarization,
- explainable AI reasoning,
- category-specific product fit,
- competitor intelligence,
- CRM history,
- follow-up actions,
- and impact metrics showing reduced manual research time.

For the MVP, financial, news, and social signals are modeled as proxy signals from public/source-backed prospect data. In production, these same backend objects can connect to live APIs such as financial datasets, news APIs, Google Business/Profile data, review platforms, LinkedIn, and CRM tools.

Production API note: MVP uses proxy signals. Production connects to financial APIs, news APIs, LinkedIn, Instagram, Google Reviews, and CRM systems.
