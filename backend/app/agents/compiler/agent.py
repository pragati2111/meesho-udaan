"""
Blueprint Compiler Agent.

Responsibility: Assemble all agent outputs into the final
BusinessBlueprint. No LLM call — pure data assembly.

Input:  all agent outputs from state
Output: blueprint_id, blueprint_ready, current_step
"""

import logging
import time
import uuid
from datetime import datetime

from app.models.blueprint import (
    BusinessBlueprint,
    ProductRecommendation,
    MarketInsight,
    PricingStrategy,
    BrandIdentity,
    ListingContent,
    GrowthPlan,
    AgentResult,
)

logger = logging.getLogger(__name__)


def run(state: dict) -> dict:
    agent_id = "compiler_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    try:
        skill = state.get("skill_profile") or {}
        market = state.get("market_intelligence") or {}
        trend = state.get("trend_analysis") or {}
        strategy = state.get("business_strategy") or {}
        pricing = state.get("pricing_strategy") or {}
        brand = state.get("brand_identity") or {}
        listing = state.get("listing_content") or {}
        growth = state.get("growth_plan") or {}

        blueprint = BusinessBlueprint(
            id=str(uuid.uuid4()),
            skill_input=state.get("skill_text", ""),
            created_at=datetime.utcnow(),
            product=ProductRecommendation(
                name=strategy.get("recommended_product", ""),
                category=skill.get("skill_category", ""),
                description=strategy.get("product_description", ""),
                target_audience=strategy.get("target_segment", ""),
                unique_selling_point=strategy.get("differentiation_strategy", ""),
            ),
            market=MarketInsight(
                demand_level=market.get("demand_level", "medium"),
                trend=trend.get("trend_direction", "stable"),
                competitors=market.get("competitor_count", 0),
                opportunity=market.get("platform_opportunity", ""),
                seasonality=", ".join(trend.get("seasonal_peaks", [])),
            ),
            pricing=PricingStrategy(
                base_price=pricing.get("base_price", 0),
                recommended_price=pricing.get("recommended_price", 0),
                premium_price=pricing.get("premium_price", 0),
                currency=pricing.get("currency", "INR"),
                margin_percentage=pricing.get("margin_percentage", 0),
                rationale=pricing.get("pricing_rationale", ""),
            ),
            brand=BrandIdentity(
                brand_name=brand.get("brand_name", ""),
                tagline=brand.get("tagline", ""),
                color_palette=brand.get("color_palette", []),
                tone_of_voice=brand.get("tone_of_voice", ""),
                target_persona=brand.get("target_persona", ""),
            ),
            listing=ListingContent(
                title=listing.get("title", ""),
                description=listing.get("description", ""),
                keywords=listing.get("keywords", []),
                hindi_title=listing.get("hindi_title", ""),
                hindi_description=listing.get("hindi_description", ""),
            ),
            growth=GrowthPlan(
                week1=growth.get("week1_actions", []),
                month1=growth.get("month1_actions", []),
                month3=growth.get("month3_actions", []),
                channels=growth.get("recommended_channels", []),
            ),
            agents=[
                AgentResult(
                    agent_id=k,
                    agent_name=k.replace("_", " ").title(),
                    status="completed",
                    duration_ms=0,
                )
                for k in [
                    "skill_agent", "market_agent", "trend_agent",
                    "strategy_agent", "pricing_agent", "branding_agent",
                    "listing_agent", "growth_agent",
                ]
            ],
        )

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"blueprint_id={blueprint.id} | "
            f"duration={duration_ms}ms"
        )

        return {
            "blueprint_id": blueprint.id,
            "blueprint_ready": True,
            "compiled_blueprint": blueprint.model_dump(mode="json"),
            "current_step": "complete",
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "blueprint_ready": False,
            "current_step": "failed",
        }