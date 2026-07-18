"""
Trend Analysis Agent.

Input:  skill_profile, market_intelligence
Output: trend_analysis
"""

import json
import logging
import time

from app.agents.trend.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.trend.schemas import TrendAnalysis
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = TrendAnalysis(
    trend_direction="growing",
    growth_rate_estimate="15% YoY",
    seasonal_peaks=["Navratri", "Diwali", "Eid"],
    emerging_niches=["handmade", "sustainable", "ethnic"],
    consumer_sentiment="Positive — buyers prefer authentic Indian crafts",
    recommended_launch_window="45 days before the next major festival",
    trend_rationale="Fallback trend assessment due to analysis error.",
)


def run(state: dict) -> dict:
    agent_id = "trend_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    skill_profile = state.get("skill_profile") or {}
    market_intelligence = state.get("market_intelligence") or {}

    try:
        llm = get_llm(temperature=0.3)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(skill_profile, market_intelligence)},
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
        trend_analysis = TrendAnalysis(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"trend={trend_analysis.trend_direction} | "
            f"duration={duration_ms}ms"
        )

        return {
            "trend_analysis": trend_analysis.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "trend_analysis": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "trend_analysis": _FALLBACK.model_dump(),
        }