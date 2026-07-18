"""
Pricing Agent.

Input:  business_strategy, market_intelligence
Output: pricing_strategy
"""

import json
import logging
import time

from app.agents.pricing.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.pricing.schemas import PricingStrategy
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = PricingStrategy(
    base_price=299.0,
    recommended_price=499.0,
    premium_price=749.0,
    currency="INR",
    margin_percentage=35.0,
    pricing_rationale="Fallback pricing based on Meesho mid-range handmade category.",
    discount_strategy="Offer 10% discount during Navratri and Diwali seasons.",
)


def run(state: dict) -> dict:
    agent_id = "pricing_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    business_strategy = state.get("business_strategy") or {}
    market_intelligence = state.get("market_intelligence") or {}

    try:
        llm = get_llm(temperature=0.1)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(business_strategy, market_intelligence),
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
        pricing_strategy = PricingStrategy(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"price=Rs {pricing_strategy.recommended_price} | "
            f"margin={pricing_strategy.margin_percentage}% | "
            f"duration={duration_ms}ms"
        )

        return {
            "pricing_strategy": pricing_strategy.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "pricing_strategy": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "pricing_strategy": _FALLBACK.model_dump(),
        }