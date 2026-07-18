from app.models.blueprint import (
    BusinessBlueprint, ProductRecommendation, MarketInsight,
    PricingStrategy, BrandIdentity, ListingContent, GrowthPlan, AgentResult
)


def generate_mock_blueprint(skill_text: str) -> BusinessBlueprint:
    """
    Returns a realistic mock blueprint.
    In Phase 5 this function gets replaced by the LangGraph agent pipeline.
    The shape of the return value stays identical — frontend never needs to change.
    """
    return BusinessBlueprint(
        skill_input=skill_text,
        product=ProductRecommendation(
            name="Hand Block-Print Ethnic Kidswear",
            category="Kids Fashion",
            description=(
                "Handcrafted ethnic wear for children featuring traditional "
                "block prints. Premium cotton fabric — perfect for festive occasions."
            ),
            target_audience="Parents of children aged 2–12 in Tier-2 & Tier-3 cities",
            unique_selling_point=(
                "Every piece is hand block-printed — no two are identical. "
                "Supports Indian artisan heritage."
            ),
        ),
        market=MarketInsight(
            demand_level="high",
            trend="growing",
            competitors=340,
            opportunity=(
                "Festive kidswear is underserved in the ₹400–₹800 range on Meesho. "
                "Demand spikes 3x before Navratri, Diwali, and Eid."
            ),
            seasonality="Peak: Sep–Nov, Jan–Feb",
        ),
        pricing=PricingStrategy(
            base_price=320,
            recommended_price=549,
            premium_price=749,
            margin_percentage=42,
            rationale=(
                "At ₹549, you capture festive buyers seeking quality. "
                "Your margin of 42% is sustainable for handcrafted goods."
            ),
        ),
        brand=BrandIdentity(
            brand_name="Rang Jaipur",
            tagline="Handcrafted with love. Worn with pride.",
            color_palette=["#9F2089", "#F2A93B", "#2E7D32", "#F5F0E8"],
            tone_of_voice="Warm, artisan, rooted in heritage — yet modern and aspirational",
            target_persona="Mothers who want their children dressed in something meaningful",
        ),
        listing=ListingContent(
            title="Rang Jaipur Hand Block-Print Cotton Kurta for Kids | Festive Ethnic Wear | 2–12 Years",
            description=(
                "Dress your little one in the magic of traditional Indian craftsmanship.\n\n"
                "✅ Hand block-printed by artisans\n"
                "✅ Pure cotton — soft, breathable, washable\n"
                "✅ Available in sizes 2–12 years\n"
                "✅ Perfect for Navratri, Diwali, Eid, and daily wear"
            ),
            keywords=[
                "kids ethnic wear", "block print kurta",
                "children festive dress", "hand printed kurta", "rajasthani kids wear"
            ],
            hindi_title="रंग जयपुर हाथ से छपा कुर्ता बच्चों के लिए | त्योहारी पोशाक",
        ),
        growth=GrowthPlan(
            week1=[
                "List 3 products on Meesho with photos on white background",
                "Share listings in 3 local WhatsApp mom groups",
                "Ask 5 existing customers for reviews",
            ],
            month1=[
                "Enroll in Meesho Supplier program for faster payouts",
                "Create Instagram Reels showing the block-printing process",
                "Launch Navratri special collection with 10% bundle discount",
            ],
            month3=[
                "Expand to custom orders via Meesho chat",
                "Partner with a local school for bulk uniform orders",
                "Hire one helper for block-printing to scale production",
            ],
            channels=["Meesho", "WhatsApp", "Instagram Reels", "Local schools"],
        ),
        agents=[
            AgentResult(agent_id="skill", agent_name="Skill Discovery Agent", status="completed", duration_ms=1243),
            AgentResult(agent_id="market", agent_name="Market Intelligence Agent", status="completed", duration_ms=1876),
            AgentResult(agent_id="trend", agent_name="Trend Analysis Agent", status="completed", duration_ms=1102),
            AgentResult(agent_id="strategy", agent_name="Business Strategy Agent", status="completed", duration_ms=2341),
            AgentResult(agent_id="pricing", agent_name="Pricing Agent", status="completed", duration_ms=987),
            AgentResult(agent_id="branding", agent_name="Branding Agent", status="completed", duration_ms=1654),
            AgentResult(agent_id="listing", agent_name="Listing Generation Agent", status="completed", duration_ms=2109),
            AgentResult(agent_id="growth", agent_name="Growth Coach Agent", status="completed", duration_ms=1432),
        ],
    )