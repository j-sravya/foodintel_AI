from __future__ import annotations

from datetime import datetime, timedelta
from hashlib import sha1

from .data_store import all_prospects, backend_rows, find_prospect, product_catalog, prospects_for_area


CATEGORY_PROFILES = {
    "Packaging": {
        "company": "FreshPack Solutions",
        "username": "packaging.rep@foodintel.ai",
        "password": "packaging123",
        "product_focus": "Leak-proof packaging",
        "products": ["Leak-proof containers", "Biryani boxes", "Cups and lids", "Thermal bags"],
        "signal_keywords": ["leakage", "spillage", "delivery", "takeaway", "temperature", "packaging"],
        "competitors": ["UFlex", "Huhtamaki", "Pactiv Evergreen", "Dart Container", "local disposable wholesalers"],
    },
    "Ingredients": {
        "company": "FreshSupply Ingredients",
        "username": "ingredients.rep@foodintel.ai",
        "password": "ingredients123",
        "product_focus": "Quality ingredients",
        "products": ["Rice", "Spices", "Sauces", "Cheese", "Ready-to-use bases"],
        "signal_keywords": ["menu", "taste", "quality", "stock", "wastage", "consistency"],
        "competitors": ["Metro Wholesale", "Reliance Smart Bazaar B2B", "Udaan", "local mandi traders"],
    },
    "Bakery Ingredients": {
        "company": "BakePro Ingredients",
        "username": "bakery.rep@foodintel.ai",
        "password": "bakery123",
        "product_focus": "Bakery ingredients",
        "products": ["Flour", "Cream", "Butter", "Chocolate", "Cake premix"],
        "signal_keywords": ["cake", "dessert", "bakery", "cream", "festival", "wastage"],
        "competitors": ["Puratos", "Dawn Foods", "Rich Products", "local bakery wholesalers"],
    },
    "Beverages": {
        "company": "BrewMix Beverages",
        "username": "beverages.rep@foodintel.ai",
        "password": "beverages123",
        "product_focus": "Cafe and beverage supplies",
        "products": ["Coffee beans", "Tea premix", "Syrups", "Shake bases", "Cold beverage cups"],
        "signal_keywords": ["coffee", "tea", "juice", "shake", "beverage", "combo"],
        "competitors": ["Nestle Professional", "Monin", "Davinci Gourmet", "local beverage distributors"],
    },
    "Cleaning / Hygiene Supplies": {
        "company": "SafeServe Hygiene",
        "username": "hygiene.rep@foodintel.ai",
        "password": "hygiene123",
        "product_focus": "Food-safe hygiene supplies",
        "products": ["Food-safe sanitizer", "Surface cleaner", "Gloves", "Hair nets", "Kitchen wipes"],
        "signal_keywords": ["hygiene", "clean", "safety", "kitchen", "staff", "compliance"],
        "competitors": ["Diversey", "Ecolab", "Hindustan Unilever Professional", "janitorial distributors"],
    },
    "Equipment": {
        "company": "KitchenPro Equipment",
        "username": "equipment.rep@foodintel.ai",
        "password": "equipment123",
        "product_focus": "Commercial kitchen equipment",
        "products": ["Ovens", "Mixers", "Coffee machines", "Display chillers", "Freezers"],
        "signal_keywords": ["capacity", "speed", "downtime", "expansion", "kitchen", "equipment"],
        "competitors": ["Rational", "Unox", "Blue Star", "Voltas", "local equipment dealers"],
    },
    "POS / CRM / Analytics": {
        "company": "ServeOS CRM",
        "username": "crm.rep@foodintel.ai",
        "password": "crm123",
        "product_focus": "Restaurant POS and loyalty software",
        "products": ["Billing software", "Loyalty campaigns", "WhatsApp CRM", "Review management"],
        "signal_keywords": ["billing", "repeat", "loyalty", "review", "customer", "campaign"],
        "competitors": ["Petpooja", "Posist", "UrbanPiper", "DotPe", "inresto"],
    },
    "Logistics / Cold Chain": {
        "company": "ColdRoute Logistics",
        "username": "logistics.rep@foodintel.ai",
        "password": "logistics123",
        "product_focus": "Delivery and cold-chain logistics",
        "products": ["Temperature-controlled delivery", "Route planning", "Insulated bags", "Emergency replenishment"],
        "signal_keywords": ["delivery", "cold", "late", "temperature", "route", "sla"],
        "competitors": ["Shadowfax", "LoadShare", "Dunzo for Business", "local delivery operators"],
    },
}

CATEGORY_TO_CATALOG = {
    "Packaging": "packaging and disposables",
    "Ingredients": "ingredients",
    "Bakery Ingredients": "bakery ingredients",
    "Beverages": "beverages",
    "Cleaning / Hygiene Supplies": "cleaning and hygiene supplies",
    "Equipment": "kitchen equipment",
    "POS / CRM / Analytics": "POS / CRM / loyalty software",
    "Logistics / Cold Chain": "delivery and cold-chain logistics",
}


def stable_score(seed: str, low: int = 68, high: int = 97) -> int:
    span = high - low + 1
    return low + int(sha1(seed.encode()).hexdigest(), 16) % span


def authenticate(username: str, password: str) -> dict | None:
    normalized = (username or "").strip().lower()
    for category, profile in CATEGORY_PROFILES.items():
        if profile["username"] == normalized and profile["password"] == password:
            return category_payload(category)
    return None


def category_payload(category: str) -> dict:
    profile = CATEGORY_PROFILES[category]
    return {
        "category": category,
        "sellerCompany": profile["company"],
        "productFocus": profile["product_focus"],
        "products": profile["products"],
        "username": profile["username"],
        "competitors": profile["competitors"],
    }


def catalog_entry(category: str) -> dict:
    target = CATEGORY_TO_CATALOG.get(category, category).lower()
    for item in product_catalog():
        if str(item.get("category", "")).lower() == target:
            return item
    return {}


def competitor_info(category: str) -> dict:
    entry = catalog_entry(category)
    return entry.get("competitor_info", {}) or {}


def market_examples(category: str) -> list[str]:
    return competitor_info(category).get("market_examples_to_verify") or CATEGORY_PROFILES[category]["competitors"]


def comparison_points(category: str) -> list[str]:
    return competitor_info(category).get("comparison_points") or [
        "price stability",
        "quality consistency",
        "delivery reliability",
        "replacement policy",
    ]


def list_categories() -> list[dict]:
    return [category_payload(category) for category in CATEGORY_PROFILES]


def prospect_key(prospect: dict) -> str:
    return str(prospect.get("id") or prospect.get("prospect_id") or prospect.get("name"))


def prospect_summary(prospect: dict, category: str) -> dict:
    area = prospect.get("area", "Hyderabad")
    name = prospect.get("name", "Prospect")
    score = stable_score(f"{name}:{category}:opportunity")
    risk = stable_score(f"{name}:{category}:risk", 18, 72)
    return {
        "id": prospect_key(prospect),
        "name": name,
        "area": area,
        "city": prospect.get("city", "Hyderabad"),
        "type": prospect.get("type") or prospect.get("business_type") or prospect.get("segment", "Food business"),
        "rating": prospect.get("rating", round(stable_score(name, 38, 48) / 10, 1)),
        "opportunityScore": score,
        "riskScore": risk,
        "priority": "High" if score >= 86 else "Medium" if score >= 76 else "Watch",
        "mainOpportunity": CATEGORY_PROFILES[category]["product_focus"],
    }


def command_center(category: str, area: str | None = None) -> dict:
    prospects = prospects_for_area(area)[:24]
    if not prospects:
        prospects = all_prospects()[:24]
    meetings = []
    base = datetime.now().replace(hour=10, minute=30, second=0, microsecond=0)
    for index, prospect in enumerate(prospects[:8]):
        summary = prospect_summary(prospect, category)
        summary["meetingTime"] = (base + timedelta(hours=index % 5, days=index // 5)).strftime("%b %d, %I:%M %p")
        summary["latestSignal"] = latest_signal(summary["name"], category)
        meetings.append(summary)
    return {
        "metrics": {
            "manualResearchReduced": "82%",
            "researchTimeSavedToday": "4.5 hours",
            "briefsGenerated": 12,
            "meetingPrepSpeed": "5x faster",
        },
        "meetings": meetings,
        "alerts": smart_alerts(category),
    }


def latest_signal(name: str, category: str) -> str:
    profile = CATEGORY_PROFILES[category]
    return f"{profile['product_focus']} fit detected from menu, review and competitor signals for {name}."


def smart_alerts(category: str) -> list[dict]:
    profile = CATEGORY_PROFILES[category]
    return [
        {
            "title": f"{profile['product_focus']} opportunity cluster",
            "detail": "High-fit prospects are concentrated across Hyderabad food-service areas.",
            "confidence": 88,
            "source": "Prospect database + raw signal ranking",
        },
        {
            "title": "Competitor verification needed",
            "detail": f"Ask whether the account currently buys from {profile['competitors'][0]} or local suppliers.",
            "confidence": 81,
            "source": "Category competitor battlecard",
        },
    ]


def trust(source: str, confidence: int, why: str) -> dict:
    return {
        "source": source,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "confidence": confidence,
        "whyThisMatters": why,
    }


def source_registry(prospect: dict, category: str) -> list[dict]:
    name = prospect.get("name", "Prospect")
    area = prospect.get("area", "Hyderabad")
    return [
        {
            "sourceType": "Company listing",
            "sourceName": "FoodIntel prospect database",
            "capturedAt": "2026-06-08 19:34",
            "confidence": 90,
            "use": f"Confirms {name} as an active food-service prospect in {area}.",
        },
        {
            "sourceType": "Menu / business signal",
            "sourceName": "Public menu and category cues",
            "capturedAt": "2026-06-08 19:34",
            "confidence": 84,
            "use": f"Maps account format to {category} product-fit opportunities.",
        },
        {
            "sourceType": "Competitor signal",
            "sourceName": "Category battlecard + local supplier proxy",
            "capturedAt": "2026-06-08 19:34",
            "confidence": 81,
            "use": "Prepares the rep to verify current supplier and switching criteria.",
        },
    ]


def raw_signal_feed(prospect: dict, category: str) -> list[dict]:
    profile = CATEGORY_PROFILES[category]
    name = prospect.get("name", "this account")
    area = prospect.get("area", "Hyderabad")
    products = ", ".join(profile["products"][:3])
    return [
        {
            "topic": "Account fit",
            "signal": f"{name} is in {area}; business format and public cues indicate fit for {products}.",
            "sentiment": "Opportunity",
            "relevance": stable_score(f"{name}:{category}:fit", 82, 96),
        },
        {
            "topic": "Buyer pain",
            "signal": f"{profile['signal_keywords'][0].title()} and {profile['signal_keywords'][1]} are the strongest category-specific discovery angles.",
            "sentiment": "Risk to solve",
            "relevance": stable_score(f"{name}:{category}:pain", 78, 94),
        },
        {
            "topic": "Supplier competition",
            "signal": f"Likely comparison set includes {', '.join(market_examples(category)[:3])}; verify current supplier in meeting.",
            "sentiment": "Competitive",
            "relevance": stable_score(f"{name}:{category}:competitor", 74, 91),
        },
    ]


def brief(prospect_id: str, category: str) -> dict:
    prospect = find_prospect(prospect_id=prospect_id)
    summary = prospect_summary(prospect, category)
    profile = CATEGORY_PROFILES[category]
    catalog = catalog_entry(category)
    competitors = competitor_info(category)
    menu_items = prospect.get("menu_items") or prospect.get("products") or prospect.get("known_items") or []
    if isinstance(menu_items, str):
        menu_items = [menu_items]

    changes = [
        {
            "title": "Area priority increased",
            "detail": f"{summary['area']} account cluster shows higher sales-prep priority for {profile['product_focus']}.",
            "confidence": 86,
            "source": "Area cluster model",
        },
        {
            "title": "Category pain became clearer",
            "detail": f"Signals indicate {profile['signal_keywords'][0]} and {profile['signal_keywords'][1]} should be discussed.",
            "confidence": 88,
            "source": "Menu + review proxy signals",
        },
        {
            "title": "Competitor verification needed",
            "detail": f"Comparison set includes {market_examples(category)[0]} and local suppliers to verify in meeting.",
            "confidence": 81,
            "source": "Category competitor battlecard",
        },
        {
            "title": "CRM memory changed the opening",
            "detail": "Relationship history recommends opening with operational impact instead of generic product introduction.",
            "confidence": 87,
            "source": "CRM memory layer",
        },
    ]
    pain_points = [
        {
            "pain": f"{profile['product_focus']} gap",
            "severity": "High",
            "evidence": f"Menu/review/supplier signals match {category} selling motion.",
            "trust": trust("Menu + reviews + seller catalog", 91, "This creates a clear reason for a category-specific pitch."),
        },
        {
            "pain": "Supplier comparison risk",
            "severity": "Medium",
            "evidence": f"Likely alternatives: {', '.join(profile['competitors'][:3])}.",
            "trust": trust("Category competitor intelligence", 84, "The rep should prepare comparison points before pricing is discussed."),
        },
        {
            "pain": "Manual follow-up leakage",
            "severity": "Medium",
            "evidence": "Previous meeting context and next steps are easy to lose without CRM memory.",
            "trust": trust("CRM memory layer", 87, "Follow-up quality directly affects conversion after the meeting."),
        },
    ]
    product_matches = [
        {
            "product": product,
            "matchScore": stable_score(f"{summary['name']}:{category}:{product}", 72, 96),
            "reason": f"{product} aligns with {summary['type']} needs and {profile['product_focus'].lower()} signals.",
            "trust": trust("Product catalog + prospect profile", stable_score(product, 80, 94), "Product-fit scoring helps avoid generic pitching."),
        }
        for product in profile["products"]
    ]
    insights = [
        {
            "title": "Category-specific opening angle",
            "insight": f"Lead with {profile['product_focus'].lower()} because it connects directly to the logged-in seller category.",
            "trust": trust("Active category context", 94, "The app must show insights related to what the salesperson sells."),
        },
        {
            "title": "Competitor question",
            "insight": f"Ask if the account currently uses {profile['competitors'][0]}, {profile['competitors'][1]}, or local suppliers.",
            "trust": trust("Competitor battlecard", 86, "Competitor discovery improves objection handling and positioning."),
        },
    ]
    suggested_questions = [
        f"What is your current process for buying {profile['product_focus'].lower()}?",
        f"Which supplier issue would make you consider switching in the {category} category?",
        "What matters more for this purchase: price, reliability, quality, service, or replacement policy?",
    ]
    return {
        "context": {
            "seller": profile["company"],
            "category": category,
            "activeProspect": summary["name"],
            "meeting": "Today 3:00 PM",
            "productFocus": profile["product_focus"],
        },
        "accountSnapshot": {
            "businessType": summary["type"],
            "area": summary["area"],
            "rating": summary["rating"],
            "targetBuyer": "Owner / purchase manager / operations lead",
            "likelyNeed": profile["product_focus"],
            "categoryReason": f"{category} is selected because the logged-in seller represents {profile['company']}.",
        },
        "summary": summary,
        "executiveSnapshot": {
            "priority": summary["priority"],
            "opportunityScore": summary["opportunityScore"],
            "clientRisk": "Moderate" if summary["riskScore"] > 45 else "Low",
            "mainOpportunity": profile["product_focus"],
        },
        "whatChanged": changes,
        "painPoints": pain_points,
        "productMatches": sorted(product_matches, key=lambda row: row["matchScore"], reverse=True),
        "sourceRegistry": source_registry(prospect, category),
        "rawSignals": raw_signal_feed(prospect, category),
        "competitorBattlecard": {
            "likelyCompetitors": market_examples(category),
            "competitorTypes": competitors.get("likely_competitor_types", profile["competitors"]),
            "comparisonPoints": comparison_points(category),
            "whereWeWin": competitors.get(
                "our_edge",
                f"Better alignment between {profile['product_focus'].lower()}, buyer pain and pilot proof.",
            ),
            "verificationNote": competitors.get(
                "verification_note",
                "Verify the current supplier during the meeting before claiming replacement potential.",
            ),
        },
        "insights": insights,
        "strategy": {
            "opening": f"Congratulations on the growth in {summary['area']}. I prepared specifically around your {profile['product_focus'].lower()} needs so we can discuss what is useful, not a generic catalog.",
            "pitch": f"{profile['company']} helps food businesses improve {profile['product_focus'].lower()} with {', '.join(profile['products'][:3])}. For {summary['name']}, I would suggest starting with a focused pilot tied to one measurable issue.",
            "questions": suggested_questions,
            "objections": [
                "If price comes up, compare total complaint reduction and replacement cost, not only unit price.",
                "If they are happy with the current supplier, ask what they would improve if switching had no risk.",
                "If minimum order quantity is a concern, offer a small pilot or mixed-SKU starter pack.",
            ],
        },
    }


def opportunity_radar(category: str) -> dict:
    prospects = all_prospects()
    profile = CATEGORY_PROFILES[category]
    areas: dict[str, int] = {}
    for prospect in prospects:
        area = prospect.get("area", "Unknown")
        areas[area] = areas.get(area, 0) + 1
    top_areas = sorted(areas.items(), key=lambda item: item[1], reverse=True)[:8]
    opportunities = [
        {
            "name": product,
            "accounts": stable_score(f"{category}:{product}:accounts", 7, 24),
            "score": stable_score(f"{category}:{product}:score", 72, 96),
            "why": f"Strong fit for {profile['product_focus'].lower()} across Hyderabad prospects.",
        }
        for product in profile["products"]
    ]
    return {"category": category, "opportunities": opportunities, "areaClusters": top_areas}


def crm_timeline(prospect_id: str, category: str) -> dict:
    prospect = find_prospect(prospect_id=prospect_id)
    summary = prospect_summary(prospect, category)
    profile = CATEGORY_PROFILES[category]
    return {
        "prospect": summary,
        "events": [
            {
                "date": "2026-05-28",
                "title": "Discovery call completed",
                "note": f"Client asked for better comparison against current {category} supplier.",
                "aiMemory": f"Bring proof around {profile['product_focus'].lower()} and pilot terms.",
            },
            {
                "date": "2026-06-01",
                "title": "AI brief refreshed",
                "note": "New review/menu/category signals were ranked for the meeting.",
                "aiMemory": "Use the latest prospect brief instead of older notes.",
            },
            {
                "date": "2026-06-08",
                "title": "Next meeting",
                "note": f"Pitch {profile['products'][0]} with a small pilot proposal.",
                "aiMemory": "Auto-generate follow-up and CRM update after meeting.",
            },
        ],
    }


def followup(prospect_id: str, category: str) -> dict:
    active_brief = brief(prospect_id, category)
    prospect = active_brief["summary"]["name"]
    profile = CATEGORY_PROFILES[category]
    return {
        "emailSubject": f"Follow-up: {profile['product_focus']} discussion for {prospect}",
        "emailBody": (
            f"Hi,\n\nThank you for discussing {profile['product_focus'].lower()} needs for {prospect}. "
            f"Based on our conversation, I suggest a small pilot using {profile['products'][0]} and {profile['products'][1]} "
            "so your team can compare quality, reliability and commercial fit before a larger switch.\n\n"
            "I can share sample options, pricing and replacement terms as the next step.\n\nBest,\nFoodIntel Sales Team"
        ),
        "crmNote": f"Discussed {category} opportunity. Next step: send pilot proposal and confirm current supplier comparison points.",
        "tasks": [
            "Send pilot proposal",
            "Confirm decision maker and current supplier",
            "Schedule follow-up after sample review",
        ],
    }


def _keyword_score(question: str, *texts: str) -> int:
    terms = {term.strip(".,!?()").lower() for term in question.split() if len(term.strip(".,!?()")) > 3}
    haystack = " ".join(texts).lower()
    return sum(1 for term in terms if term in haystack)


def _rank_evidence(question: str, rows: list[dict], title_key: str, detail_key: str, score_key: str = "relevance") -> list[dict]:
    ranked = []
    for row in rows:
        keyword_score = _keyword_score(question, str(row.get(title_key, "")), str(row.get(detail_key, "")))
        base_score = int(row.get(score_key, row.get("confidence", row.get("matchScore", 75))) or 75)
        ranked.append((keyword_score * 10 + base_score, row))
    return [row for _, row in sorted(ranked, key=lambda item: item[0], reverse=True)]


def copilot_answer(prospect_id: str, category: str, question: str) -> dict:
    active_brief = brief(prospect_id, category)
    summary = active_brief["summary"]
    context = active_brief["context"]
    profile = CATEGORY_PROFILES[category]
    normalized = (question or "").lower()

    database_candidates = [
        {
            "title": "Active account context",
            "detail": f"{summary['name']} is a {summary['type']} in {summary['area']} with {summary['opportunityScore']}/100 opportunity score for {context['productFocus']}.",
            "relevance": 94,
        },
        {
            "title": "Best product match",
            "detail": f"{active_brief['productMatches'][0]['product']} is the strongest catalog fit because {active_brief['productMatches'][0]['reason']}",
            "relevance": active_brief["productMatches"][0]["matchScore"],
        },
        {
            "title": "CRM memory",
            "detail": "Relationship history recommends opening with operational impact and using a small pilot instead of a broad catalog pitch.",
            "relevance": 87,
        },
        {
            "title": "Competitor battlecard",
            "detail": f"Likely comparison set: {', '.join(active_brief['competitorBattlecard']['likelyCompetitors'][:4])}.",
            "relevance": 84,
        },
    ]
    database_rows = _rank_evidence(question, database_candidates, "title", "detail")[:3]

    raw_rows = _rank_evidence(question, active_brief["rawSignals"], "topic", "signal")[:3]
    internet_rows = [
        {
            "title": row["topic"],
            "detail": row["signal"],
            "source": "MVP internet/proxy signal layer",
            "confidence": row["relevance"],
        }
        for row in raw_rows
    ]
    internet_rows.append(
        {
            "title": "Production web-search connector",
            "detail": "In production this step calls search APIs, Google Reviews, delivery platforms, LinkedIn, Instagram and news sources before the AI response is generated.",
            "source": "Production API note",
            "confidence": 80,
        }
    )

    top_product = active_brief["productMatches"][0]["product"]
    if "competitor" in normalized or "compare" in normalized:
        answer = (
            f"For {summary['name']}, lead with competitor discovery before making claims. "
            f"Ask whether they currently buy from {profile['competitors'][0]}, {profile['competitors'][1]} or local suppliers, then compare on {', '.join(comparison_points(category)[:3])}."
        )
        recommendation = f"Use the competitor battlecard, but position {top_product} as a low-risk pilot instead of a direct replacement on the first call."
    elif "price" in normalized or "objection" in normalized:
        answer = (
            f"For {summary['name']}, expect price or current-supplier objections. "
            f"Anchor the conversation on measurable operational impact from {context['productFocus'].lower()}, not only unit price."
        )
        recommendation = f"Offer a small pilot using {top_product} and compare replacement cost, reliability and service response."
    elif "follow" in normalized or "email" in normalized:
        answer = (
            f"The follow-up should stay tied to the meeting goal: {context['productFocus'].lower()} for {summary['name']}. "
            "Keep it short, confirm the decision maker, and propose a sample-review date."
        )
        recommendation = "Send one pilot proposal, one decision-maker confirmation question and one follow-up date."
    else:
        answer = (
            f"For {summary['name']}, pitch {context['productFocus'].lower()} through a focused pilot. "
            f"Start with {top_product}, connect it to the category-specific pain signals, then ask about current supplier reliability and switching criteria."
        )
        recommendation = f"Open with the strongest product fit, then use source-backed questions before discussing pricing."

    sources = [
        {
            "name": source["sourceName"],
            "type": source["sourceType"],
            "timestamp": source["capturedAt"],
            "confidence": source["confidence"],
        }
        for source in active_brief["sourceRegistry"]
    ]
    sources.append(
        {
            "name": "Production web-search connector",
            "type": "Internet / scrape API",
            "timestamp": "Not configured in MVP",
            "confidence": "Connector-ready",
        }
    )

    return {
        "question": question,
        "workflow": [
            "Search prospect database",
            "Search internet/proxy signal layer",
            "Clean and rank evidence",
            "Send ranked context to AI reasoning layer",
            "Return structured answer with sources",
        ],
        "answer": answer,
        "fromDatabase": database_rows,
        "fromInternet": internet_rows,
        "recommendation": recommendation,
        "sources": sources,
        "productionNote": "MVP uses database records and proxy web signals. Production connects this same route to live web-search, review, social, news and CRM APIs.",
    }


def agent_workflow() -> dict:
    return {
        "layers": [
            "Data Layer",
            "Context Layer",
            "Signal Orchestration Layer",
            "AI Intelligence Layer",
            "Memory Layer",
            "Trust & Explainability Layer",
            "Workflow Automation Layer",
            "Frontend Experience Layer",
        ],
        "agents": [
            "Meeting Detection Agent",
            "Research Agent",
            "Signal Orchestration Agent",
            "Review Analysis Agent",
            "Competitor Intelligence Agent",
            "Insight Ranking Agent",
            "Sales Strategy And Follow-up Agent",
        ],
        "evidenceStore": [
            "Source registry stores company listing, menu/review, competitor and CRM evidence.",
            "Raw signals are ranked before the AI creates sales recommendations.",
            "Every major insight carries source, timestamp, confidence and why-this-matters text.",
            "Brief versions and CRM memory support what-changed-since-last-meeting reasoning.",
        ],
        "productionNote": "MVP uses proxy signals. Production connects to financial APIs, news APIs, LinkedIn, Instagram, Google Reviews, delivery platforms, CRM systems, Supabase, PostHog and Stripe.",
    }
