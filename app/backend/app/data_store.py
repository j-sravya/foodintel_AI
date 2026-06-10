import json
from functools import lru_cache
from pathlib import Path

from .config import DATA_DIR


AREA_DATA_PATH = DATA_DIR / "as_rao_nagar_food_industry_dataset.json"
BACKEND_DATA_PATH = DATA_DIR / "sales_intelligence_backend.json"


@lru_cache(maxsize=1)
def load_area_data() -> dict:
    with AREA_DATA_PATH.open() as file:
        return json.load(file)


@lru_cache(maxsize=1)
def load_backend_data() -> dict:
    with BACKEND_DATA_PATH.open() as file:
        return json.load(file)


def all_prospects() -> list[dict]:
    return load_area_data().get("prospects", [])


def product_catalog() -> list[dict]:
    return load_area_data().get("product_catalog", [])


def unique_areas() -> list[str]:
    areas = sorted({p.get("area", "Unknown") for p in all_prospects() if p.get("area")})
    return areas


def prospects_for_area(area: str | None = None) -> list[dict]:
    prospects = all_prospects()
    if area and area != "All":
        prospects = [p for p in prospects if p.get("area") == area]
    return prospects


def find_prospect(prospect_id: str | None = None, name: str | None = None) -> dict:
    prospects = all_prospects()
    if prospect_id:
        for prospect in prospects:
            if str(prospect.get("id") or prospect.get("prospect_id") or prospect.get("name")) == str(prospect_id):
                return prospect
    if name:
        for prospect in prospects:
            if prospect.get("name") == name:
                return prospect
    return prospects[0]


def backend_rows(key: str) -> list[dict]:
    value = load_backend_data().get(key, [])
    return value if isinstance(value, list) else []

