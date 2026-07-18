"""
Market Intelligence Agent.

Input:  skill_profile
Output: market_intelligence
"""

import json
import logging
import time

from app.agents.market.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.market.schemas import MarketIntelligence
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = MarketIntelligence(
    demand_level="medium",
    market_size_estimate="500 Cr annually",
    top_performing_categories=["Handicrafts", "Home Decor"],
    competitor_count=200,
    avg_competitor_price=400.0,
    platform_opportunity="Handmade products have growing demand on Meesho",
    underserved_segments=["Tier-2 buyers seeking authentic crafts"],
    demand_rationale="Fallback assessment due to analysis error.",
)


def run(state: dict) -> dict:
    agent_id = "market_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    skill_profile = state.get("skill_profile") or {}

    try:
        llm = get_llm(temperature=0.2)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(skill_profile)},
        ]

        response = llm.invoke(messages)

        # Gemini-compatible response extraction
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
        market_intelligence = MarketIntelligence(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"demand={market_intelligence.demand_level} | "
            f"duration={duration_ms}ms"
        )

        return {
            "market_intelligence": market_intelligence.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "market_intelligence": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "market_intelligence": _FALLBACK.model_dump(),
        }