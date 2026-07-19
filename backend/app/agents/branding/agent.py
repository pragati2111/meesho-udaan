"""
Branding Agent.

Input:  business_strategy, skill_profile, trend_analysis
Output: brand_identity
"""

import json
import logging
import time


from app.agents.branding.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.branding.schemas import BrandIdentity
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = BrandIdentity(
    brand_name="Kala Craft",
    tagline="Made with hands. Sold with pride.",
    color_palette=["#9F2089", "#F2A93B", "#2E7D32", "#F5F0E8"],
    tone_of_voice="Warm, authentic, rooted in Indian heritage",
    target_persona="A woman who values handmade quality over fast fashion",
    brand_story="Born from generations of craft tradition, Kala Craft brings authentic Indian artisanship to modern buyers.",
)


def run(state: dict) -> dict:
    agent_id = "branding_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    business_strategy = state.get("business_strategy") or {}
    skill_profile = state.get("skill_profile") or {}
    trend_analysis = state.get("trend_analysis") or {}

    try:
        llm = get_llm(temperature=0.85)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(
                    business_strategy, skill_profile, trend_analysis
                ),
            },
        ]

       
        response = llm.invoke(messages)

# Gemini/OpenAI compatible response extraction
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
        brand_identity = BrandIdentity(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"brand={brand_identity.brand_name} | "
            f"duration={duration_ms}ms"
        )

        return {
            "brand_identity": brand_identity.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "brand_identity": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "brand_identity": _FALLBACK.model_dump(),
        }