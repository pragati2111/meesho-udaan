"""
Trend Analysis Agent Prompts.
"""

SYSTEM_PROMPT = """You are a Trend Analysis AI for Meesho Udaan.

You analyze Indian ecommerce trends and recommend the best launch timing.

Consider:
- Vocal for Local movement
- Sustainable fashion growth
- Festival shopping seasons
- Tier-2 and Tier-3 buyer behavior
- Meesho marketplace trends
- Handmade product demand

Return ONLY valid JSON.

{
  "trend_direction": "declining|stable|growing|viral",
  "growth_rate_estimate": "string",
  "seasonal_peaks": ["string"],
  "emerging_niches": ["string"],
  "consumer_sentiment": "string",
  "recommended_launch_window": "string",
  "trend_rationale": "string"
}
"""


def build_user_prompt(skill_profile: dict | None, market_intelligence: dict | None) -> str:
    """
    Safe prompt builder.

    Handles None values gracefully.
    """

    skill_profile = skill_profile or {}
    market_intelligence = market_intelligence or {}

    skill_name = skill_profile.get("skill_name", "")
    category = skill_profile.get("skill_category", "")
    products = ", ".join(skill_profile.get("sellable_products", []))

    demand = market_intelligence.get("demand_level", "unknown")
    categories = ", ".join(
        market_intelligence.get("top_performing_categories", [])
    )

    return f"""
Analyze Indian ecommerce trends.

Skill:
{skill_name}

Category:
{category}

Sellable Products:
{products}

Current Demand:
{demand}

Top Categories:
{categories}

Respond ONLY with the JSON object.
"""