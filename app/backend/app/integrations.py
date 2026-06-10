from .config import get_settings


def track_posthog_event(event: str, properties: dict) -> dict:
    settings = get_settings()
    if not settings.posthog_key:
        return {
            "mode": "demo",
            "sent": False,
            "note": "POSTHOG_KEY is not configured, so the event was accepted locally only.",
        }

    payload = {
        "api_key": settings.posthog_key,
        "event": event,
        "properties": {
            "distinct_id": properties.get("distinct_id", "demo-sales-rep"),
            **properties,
        },
    }
    try:
        import urllib.request

        request = urllib.request.Request(
            "https://app.posthog.com/capture/",
            data=__import__("json").dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=8) as response:
            response.read()
        return {"mode": "posthog", "sent": True}
    except Exception as error:
        return {
            "mode": "posthog",
            "sent": False,
            "note": (
                "PostHog event accepted by the backend. Live server-side delivery failed in this local "
                f"environment, usually because of local SSL certificates: {error}. The React frontend "
                "also sends events through posthog-js when VITE_POSTHOG_KEY is configured."
            ),
        }


def create_stripe_checkout(plan_name: str) -> dict:
    settings = get_settings()
    price_lookup = {
        "Starter": settings.stripe_price_starter,
        "Growth": settings.stripe_price_growth,
        "Enterprise": settings.stripe_price_enterprise,
    }
    price_id = price_lookup.get(plan_name)
    if not settings.stripe_secret_key or not price_id:
        return {
            "mode": "demo",
            "checkoutUrl": "",
            "message": f"Stripe demo mode: add STRIPE_SECRET_KEY and STRIPE_PRICE_{plan_name.upper()} to enable live checkout.",
        }

    try:
        import stripe
    except ImportError:
        return {
            "mode": "demo",
            "checkoutUrl": "",
            "message": "Stripe package is not installed. Billing remains in demo mode.",
        }

    stripe.api_key = settings.stripe_secret_key
    checkout = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=settings.stripe_success_url,
        cancel_url=settings.stripe_cancel_url,
        metadata={"product": "FoodIntel AI", "plan": plan_name},
    )
    return {"mode": "stripe", "checkoutUrl": checkout.url, "message": "Redirecting to Stripe Checkout."}
