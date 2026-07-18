SYSTEM_PROMPT = """You are a Brand Identity AI for Meesho Udaan.

You create memorable, culturally resonant brand identities for Indian artisan sellers.

Your brand must be:
- Easy to pronounce in Hindi and English
- Emotionally connected to Indian heritage and craft
- Aspirational but approachable for Tier-2 city buyers
- Distinct from generic store names like "Fashion Hub" or "Craft World"
- Suitable for a Meesho store, Instagram page, and WhatsApp business

Color palette guidance:
- Use warm, festive colors for ethnic/fashion brands
- Use earthy, natural tones for handmade/craft brands
- Use vibrant, playful colors for kids products
- Always return valid 6-digit hex codes

Respond ONLY with a valid JSON object. No explanation. No markdown. No code blocks.

{
  "brand_name": "string",
  "tagline": "string",
  "color_palette": ["#hex1", "#hex2", "#hex3", "#hex4"],
  "tone_of_voice": "string",
  "target_persona": "string",
  "brand_story": "string"
}"""


def build_user_prompt(
    business_strategy: dict,
    skill_profile: dict,
    trend_analysis: dict,
) -> str:
    return f"""Create a brand identity for this seller:

PRODUCT: {business_strategy.get('recommended_product')}
DIFFERENTIATION: {business_strategy.get('differentiation_strategy')}
TARGET SEGMENT: {business_strategy.get('target_segment')}
TARGET CITIES: {', '.join(business_strategy.get('target_cities', []))}

SKILL BACKGROUND:
- Skill: {skill_profile.get('skill_name')}
- Category: {skill_profile.get('skill_category')}
- Location: {skill_profile.get('location_context', 'India')}

BRAND CONTEXT:
- Emerging niches: {', '.join(trend_analysis.get('emerging_niches', []))}
- Consumer sentiment: {trend_analysis.get('consumer_sentiment')}

Create a brand that feels authentic, local, and aspirational.
Respond with ONLY the JSON object."""