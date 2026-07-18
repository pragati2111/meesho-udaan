"""
Listing Generation Agent Prompts.
"""

SYSTEM_PROMPT = """You are a Product Listing AI for Meesho Udaan.

Write high-converting Meesho listings.

Requirements:

- Attractive title
- SEO keywords
- Emotional description
- Hindi translation
- Category path

Return ONLY valid JSON.

{
  "title": "string",
  "description": "string",
  "keywords": ["string"],
  "hindi_title": "string",
  "hindi_description": "string",
  "category_path": "string"
}
"""


def build_user_prompt(
    business_strategy: dict | None,
    brand_identity: dict | None,
    pricing_strategy: dict | None,
) -> str:
    """
    Safe prompt builder.

    Handles None values gracefully.
    """

    business_strategy = business_strategy or {}
    brand_identity = brand_identity or {}
    pricing_strategy = pricing_strategy or {}

    return f"""
Write a complete Meesho listing.

PRODUCT
--------
Name:
{business_strategy.get("recommended_product", "")}

Description:
{business_strategy.get("product_description", "")}

Target Segment:
{business_strategy.get("target_segment", "")}

USP:
{business_strategy.get("differentiation_strategy", "")}


BRAND
------
Name:
{brand_identity.get("brand_name", "")}

Tagline:
{brand_identity.get("tagline", "")}

Tone:
{brand_identity.get("tone_of_voice", "")}

Persona:
{brand_identity.get("target_persona", "")}


PRICING
--------
Recommended Price:
₹{pricing_strategy.get("recommended_price", "")}

Premium Price:
₹{pricing_strategy.get("premium_price", "")}


Generate:

- Title
- Description
- Keywords
- Hindi Title
- Hindi Description
- Category Path

Respond ONLY with the JSON object.
"""