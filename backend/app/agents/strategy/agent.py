"""
Business Strategy Agent.

Input: skill_profile, market_intelligence, trend_analysis
Output: business_strategy
"""

import json
import logging
import time

from app.agents.strategy.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.strategy.schemas import BusinessStrategy
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = BusinessStrategy(
    recommended_product="Handmade Ethnic Wear",
    product_description="Handcrafted ethnic clothing using traditional techniques.",
    business_model="D2C via Meesho",
    target_segment="Women aged 18-40 in Tier-2 cities",
    target_cities=["Jaipur", "Surat", "Lucknow", "Indore"],
    differentiation_strategy="Authentic handmade quality at affordable prices",
    key_risks=[
        "Seasonal demand",
        "Competition from machine-made alternatives",
    ],
    rationale="Fallback strategy due to analysis error.",
)


def run(state: dict) -> dict:
    agent_id = "strategy_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    skill_profile = state.get("skill_profile") or {}
    market_intelligence = state.get("market_intelligence") or {}
    trend_analysis = state.get("trend_analysis") or {}

    try:
        llm = get_llm(temperature=0.4)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_user_prompt(
                    skill_profile,
                    market_intelligence,
                    trend_analysis,
                ),
            },
        ]

        response = llm.invoke(messages)

        # ==========================================================
        # Gemini/OpenAI compatible response extraction
        # ==========================================================
        if isinstance(response.content, str):
            raw_content = response.content

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

        business_strategy = BusinessStrategy(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)

        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"product={business_strategy.recommended_product} | "
            f"duration={duration_ms}ms"
        )

        return {
            "business_strategy": business_strategy.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)

        logger.error(
            f"[{agent_id}] JSON parse failed | "
            f"{str(e)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "errors": {
                **state.get("errors", {}),
                agent_id: f"JSON parse error: {str(e)}",
            },
            "current_step": agent_id,
            "business_strategy": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)

        logger.error(
            f"[{agent_id}] FAILED | "
            f"{str(e)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "errors": {
                **state.get("errors", {}),
                agent_id: str(e),
            },
            "current_step": agent_id,
            "business_strategy": _FALLBACK.model_dump(),
        }