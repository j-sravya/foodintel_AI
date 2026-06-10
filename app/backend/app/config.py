from functools import lru_cache
import os
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
PROJECT_DIR = ROOT_DIR
DATA_DIR = PROJECT_DIR / "data"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


load_env_file(PROJECT_DIR / ".env")
load_env_file(PROJECT_DIR.parent / ".env")


class Settings:
    def __init__(
        self,
        app_name: str = "FoodIntel AI",
        api_version: str = "production-demo-v1",
        supabase_url: str = "",
        supabase_anon_key: str = "",
        posthog_key: str = "",
        stripe_publishable_key: str = "",
        stripe_secret_key: str = "",
        stripe_success_url: str = "http://localhost:5173?checkout=success",
        stripe_cancel_url: str = "http://localhost:5173?checkout=cancelled",
        stripe_price_starter: str = "",
        stripe_price_growth: str = "",
        stripe_price_enterprise: str = "",
    ):
        self.app_name = app_name
        self.api_version = api_version
        self.supabase_url = supabase_url
        self.supabase_anon_key = supabase_anon_key
        self.posthog_key = posthog_key
        self.stripe_publishable_key = stripe_publishable_key
        self.stripe_secret_key = stripe_secret_key
        self.stripe_success_url = stripe_success_url
        self.stripe_cancel_url = stripe_cancel_url
        self.stripe_price_starter = stripe_price_starter
        self.stripe_price_growth = stripe_price_growth
        self.stripe_price_enterprise = stripe_price_enterprise


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
    return Settings(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_anon_key=os.getenv("SUPABASE_ANON_KEY", ""),
        posthog_key=os.getenv("POSTHOG_KEY", ""),
        stripe_publishable_key=os.getenv("STRIPE_PUBLISHABLE_KEY", ""),
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
        stripe_success_url=os.getenv("STRIPE_SUCCESS_URL", f"{frontend_url}?checkout=success"),
        stripe_cancel_url=os.getenv("STRIPE_CANCEL_URL", f"{frontend_url}?checkout=cancelled"),
        stripe_price_starter=os.getenv("STRIPE_PRICE_STARTER", ""),
        stripe_price_growth=os.getenv("STRIPE_PRICE_GROWTH", ""),
        stripe_price_enterprise=os.getenv("STRIPE_PRICE_ENTERPRISE", ""),
    )
