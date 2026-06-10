import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlparse

from app.domain import (
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
from app.config import get_settings
from app.data_store import product_catalog, unique_areas
from app.integrations import create_stripe_checkout, track_posthog_event


def json_response(handler, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class FoodIntelHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        json_response(self, {})

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        category = query.get("category", ["Packaging"])[0]
        area = query.get("area", [None])[0]
        if area:
            area = unquote(area)

        try:
            if path == "/health":
                settings = get_settings()
                return json_response(self, {
                    "status": "ok",
                    "service": "FoodIntel AI production backend",
                    "runtime": "simple_api",
                    "integrations": {
                        "supabaseConfigured": bool(settings.supabase_url and settings.supabase_anon_key),
                        "posthogConfigured": bool(settings.posthog_key),
                        "stripeConfigured": bool(settings.stripe_secret_key),
                    },
                })
            if path == "/categories":
                return json_response(self, {"categories": list_categories()})
            if path.startswith("/catalog/"):
                selected = unquote(path.split("/catalog/", 1)[1])
                return json_response(self, {
                    "category": selected,
                    "profile": category_payload(selected),
                    "catalog": product_catalog(),
                })
            if path == "/areas":
                return json_response(self, {"areas": unique_areas()})
            if path == "/prospects":
                rows = [prospect_summary(p, category) for p in prospects_for_area(area)[:80]]
                return json_response(self, {"prospects": rows})
            if path == "/command-center":
                return json_response(self, command_center(category, area))
            if path.startswith("/brief/"):
                prospect_id = unquote(path.split("/brief/", 1)[1])
                return json_response(self, brief(prospect_id, category))
            if path == "/opportunity-radar":
                return json_response(self, opportunity_radar(category))
            if path.startswith("/crm-timeline/"):
                prospect_id = unquote(path.split("/crm-timeline/", 1)[1])
                return json_response(self, crm_timeline(prospect_id, category))
            if path.startswith("/followup/"):
                prospect_id = unquote(path.split("/followup/", 1)[1])
                return json_response(self, followup(prospect_id, category))
            if path == "/ai-workflow":
                return json_response(self, agent_workflow())
            if path == "/billing/plans":
                return json_response(self, {
                    "plans": [
                        {"name": "Starter", "price": "₹2,999/user/month", "features": ["100 briefs/month", "Pitch downloads", "Basic CRM notes"]},
                        {"name": "Growth", "price": "₹14,999/team/month", "features": ["1,000 briefs/month", "Team dashboard", "Analytics", "Bulk prospects"]},
                        {"name": "Enterprise", "price": "Custom", "features": ["SSO", "Live APIs", "Advanced audit logs", "Custom CRM integrations"]},
                    ],
                    "note": "Production checkout is handled by Stripe.",
                })
            return json_response(self, {"detail": "Not found"}, 404)
        except Exception as error:
            return json_response(self, {"detail": str(error)}, 500)

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8") if length else "{}"
        payload = json.loads(body or "{}")

        try:
            if parsed.path == "/auth/login":
                session = authenticate(payload.get("username", ""), payload.get("password", ""))
                if not session:
                    return json_response(self, {"detail": "Invalid category login"}, 401)
                return json_response(self, {"user": session, "token": "demo-local-session-token"})
            if parsed.path == "/analytics/track":
                result = track_posthog_event(payload.get("event", ""), payload.get("properties", {}))
                return json_response(self, {
                    "accepted": True,
                    "event": payload.get("event", ""),
                    "properties": payload.get("properties", {}),
                    "delivery": result,
                })
            if parsed.path == "/billing/checkout":
                return json_response(self, create_stripe_checkout(payload.get("plan", "")))
            if parsed.path == "/copilot":
                return json_response(self, copilot_answer(
                    payload.get("prospectId", ""),
                    payload.get("category", "Packaging"),
                    payload.get("question", ""),
                ))
            return json_response(self, {"detail": "Not found"}, 404)
        except Exception as error:
            return json_response(self, {"detail": str(error)}, 500)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8787), FoodIntelHandler)
    print("FoodIntel simple API running on http://localhost:8787")
    server.serve_forever()
