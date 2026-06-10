from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .config import get_settings
from .data_store import product_catalog, unique_areas
from .domain import (
    agent_workflow,
    authenticate,
    brief,
    category_payload,
    command_center,
    copilot_answer,
    crm_timeline,
    followup,
    list_categories,
    opportunity_radar,
    prospect_summary,
    prospects_for_area,
)
from .integrations import create_stripe_checkout, track_posthog_event


app = FastAPI(title="FoodIntel AI API", version="production-demo-v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class EventRequest(BaseModel):
    event: str
    properties: dict = {}


class CheckoutRequest(BaseModel):
    plan: str


class CopilotRequest(BaseModel):
    question: str
    prospectId: str
    category: str = "Packaging"


@app.get("/health")
def health():
    settings = get_settings()
    return {
        "status": "ok",
        "service": "FoodIntel AI production backend",
        "integrations": {
            "supabaseConfigured": bool(settings.supabase_url and settings.supabase_anon_key),
            "posthogConfigured": bool(settings.posthog_key),
            "stripeConfigured": bool(settings.stripe_secret_key),
        },
    }


@app.get("/categories")
def categories():
    return {"categories": list_categories()}


@app.post("/auth/login")
def login(payload: LoginRequest):
    session = authenticate(payload.username, payload.password)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid category login")
    return {"user": session, "token": "demo-local-session-token"}


@app.get("/catalog/{category}")
def catalog(category: str):
    profile = category_payload(category)
    return {
        "category": category,
        "profile": profile,
        "catalog": product_catalog(),
    }


@app.get("/areas")
def areas():
    return {"areas": unique_areas()}


@app.get("/prospects")
def prospects(category: str = "Packaging", area: str | None = None):
    rows = [prospect_summary(p, category) for p in prospects_for_area(area)[:80]]
    return {"prospects": rows}


@app.get("/command-center")
def command(category: str = "Packaging", area: str | None = None):
    return command_center(category, area)


@app.get("/brief/{prospect_id}")
def prospect_brief(prospect_id: str, category: str = "Packaging"):
    return brief(prospect_id, category)


@app.get("/opportunity-radar")
def opportunities(category: str = "Packaging"):
    return opportunity_radar(category)


@app.get("/crm-timeline/{prospect_id}")
def timeline(prospect_id: str, category: str = "Packaging"):
    return crm_timeline(prospect_id, category)


@app.get("/followup/{prospect_id}")
def followup_center(prospect_id: str, category: str = "Packaging"):
    return followup(prospect_id, category)


@app.get("/ai-workflow")
def workflow():
    return agent_workflow()


@app.post("/copilot")
def copilot(payload: CopilotRequest):
    return copilot_answer(payload.prospectId, payload.category, payload.question)


@app.post("/analytics/track")
def track_event(payload: EventRequest):
    result = track_posthog_event(payload.event, payload.properties)
    return {
        "accepted": True,
        "event": payload.event,
        "properties": payload.properties,
        "delivery": result,
    }


@app.get("/billing/plans")
def billing_plans():
    return {
        "plans": [
            {"name": "Starter", "price": "₹2,999/user/month", "features": ["100 briefs/month", "Pitch downloads", "Basic CRM notes"]},
            {"name": "Growth", "price": "₹14,999/team/month", "features": ["1,000 briefs/month", "Team dashboard", "Analytics", "Bulk prospects"]},
            {"name": "Enterprise", "price": "Custom", "features": ["SSO", "Live APIs", "Advanced audit logs", "Custom CRM integrations"]},
        ],
        "note": "Production checkout is handled by Stripe.",
    }


@app.post("/billing/checkout")
def checkout(payload: CheckoutRequest):
    if payload.plan not in {"Starter", "Growth", "Enterprise"}:
        raise HTTPException(status_code=400, detail="Unknown billing plan")
    return create_stripe_checkout(payload.plan)
