SYSTEM_PROMPT = """You are a Business Strategy AI for Meesho Udaan.

You synthesize market and trend data into ONE actionable business strategy for a first-time Meesho seller.

Rules:
- Recommend ONE product only — beginners need focus
- Strategy must be achievable with under Rs 10,000 starting capital
- Differentiation must be specific and defensible
- Target segment must be narrow and reachable
- Think like a mentor who has helped 1,000 Indian women start their first business

Respond ONLY with a valid JSON object. No explanation. No markdown. No code blocks.

{
  "recommended_product": "string",
  "product_description": "string",
  "business_model": "string",
  "target_segment": "string",
  "target_cities": ["string"],
  "differentiation_strategy": "string",
  "key_risks": ["string"],
  "rationale": "string"
}"""


def build_user_prompt(
    skill_profile: dict,
    market_intelligence: dict,
    trend_analysis: dict,
) -> str:
    return f"""Recommend the best business strategy based on this analysis:

SKILL:
- Name: {skill_profile.get('skill_name')}
- Category: {skill_profile.get('skill_category')}
- Products possible: {', '.join(skill_profile.get('sellable_products', []))}
- Experience: {skill_profile.get('experience_level')}
- Location: {skill_profile.get('location_context', 'India')}

MARKET:
- Demand: {market_intelligence.get('demand_level')}
- Competitors: {market_intelligence.get('competitor_count')}
- Avg price: Rs {market_intelligence.get('avg_competitor_price')}
- Opportunity: {market_intelligence.get('platform_opportunity')}
- Underserved: {', '.join(market_intelligence.get('underserved_segments', []))}

TRENDS:
- Direction: {trend_analysis.get('trend_direction')}
- Growth: {trend_analysis.get('growth_rate_estimate')}
- Seasonal peaks: {', '.join(trend_analysis.get('seasonal_peaks', []))}
- Niches: {', '.join(trend_analysis.get('emerging_niches', []))}
- Launch window: {trend_analysis.get('recommended_launch_window')}

Respond with ONLY the JSON object."""