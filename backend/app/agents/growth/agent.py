"""
Growth Coach Agent.

Input:  business_strategy, pricing_strategy, brand_identity, trend_analysis
Output: growth_plan
"""

import json
import logging
import time

from app.agents.growth.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.growth.schemas import GrowthPlan
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = GrowthPlan(
    week1_actions=[
        "List 3 products on Meesho with clean white-background photos",
        "Create a WhatsApp Business profile with your brand name",
        "Share your Meesho store link in 3 local WhatsApp groups",
    ],
    month1_actions=[
        "Get 5 reviews from friends and family who buy your product",
        "Create 2 Instagram Reels showing your making process",
        "Enroll in Meesho Supplier program for faster payouts",
    ],
    month3_actions=[
        "Launch a festive collection timed to the next major festival",
        "Partner with one local school or organization for bulk order",
        "Consider hiring one part-time helper to scale production",
    ],
    recommended_channels=["Meesho", "WhatsApp Business", "Instagram Reels"],
    first_revenue_estimate="Rs 5,000 - Rs 10,000 in the first month with consistent effort",
    scale_trigger="When you receive more than 10 orders per week consistently",
)


def run(state: dict) -> dict:
    agent_id = "growth_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    business_strategy = state.get("business_strategy") or {}
    pricing_strategy = state.get("pricing_strategy") or {}
    brand_identity = state.get("brand_identity") or {}
    trend_analysis = state.get("trend_analysis") or {}

    try:
        llm = get_llm(temperature=0.5)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(
                    business_strategy,
                    pricing_strategy,
                    brand_identity,
                    trend_analysis,
                ),
            },
        ]

        response = llm.invoke(messages)

        if hasattr(response, "text") and response.text:
            raw_content = response.text
        elif isinstance(response.content, list):
            raw_content = ""
            for item in response.content:
                if isinstance(item, dict):
                    raw_content += item.get("text", "")
                else:
                    raw_content += str(item)
        else:
            raw_content = str(response.content)

        raw_content = raw_content.strip()

        if raw_content.startswith("```"):
            raw_content = raw_content.replace("```json", "")
            raw_content = raw_content.replace("```", "")
            raw_content = raw_content.strip()

        parsed = json.loads(raw_content)
        growth_plan = GrowthPlan(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"channels={len(growth_plan.recommended_channels)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "growth_plan": growth_plan.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "growth_plan": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "growth_plan": _FALLBACK.model_dump(),
        }