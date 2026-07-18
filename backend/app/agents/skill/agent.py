"""
Skill Discovery Agent.

Responsibility: Extract a structured SkillProfile from raw user input.

Input state fields used:
  - skill_text
  - language

Output state fields written:
  - skill_profile
  - current_step
  - errors (only on failure)
"""

import json
import logging
import time

from app.agents.skill.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.skill.schemas import SkillProfile
from app.services.llm import get_llm

logger = logging.getLogger(__name__)


def run(state: dict) -> dict:
    """
    Skill Discovery Agent node function.

    Reads raw skill input from state.
    Returns structured SkillProfile written into state.

    Args:
        state: Current graph state dict

    Returns:
        Dict with keys to merge into shared state
    """
    agent_id = "skill_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    # ─────────────────────────────────────────────────────────────
    # Read inputs
    # ─────────────────────────────────────────────────────────────
    skill_text = state.get("skill_text")
    language = state.get("language", "en")

    if not skill_text:
        logger.warning(f"[{agent_id}] No skill_text found in state")
        return {
            "errors": {
                **state.get("errors", {}),
                agent_id: "No skill input provided",
            },
            "current_step": agent_id,
        }

    try:
        llm = get_llm(temperature=0.3)

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": build_user_prompt(skill_text, language),
            },
        ]

        response = llm.invoke(messages)

        # ==========================================================
        # Gemini/OpenAI compatible response extraction
        # ==========================================================
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

        logger.debug(f"[{agent_id}] Raw LLM response:\n{raw_content}")

        # ==========================================================
        # Remove markdown code blocks if present
        # ==========================================================
        if raw_content.startswith("```"):
            raw_content = raw_content.replace("```json", "")
            raw_content = raw_content.replace("```", "")
            raw_content = raw_content.strip()

        # ==========================================================
        # Parse JSON
        # ==========================================================
        parsed = json.loads(raw_content)

        skill_profile = SkillProfile(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)

        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"skill={skill_profile.skill_name} | "
            f"category={skill_profile.skill_category} | "
            f"duration={duration_ms}ms"
        )

        return {
            "skill_profile": skill_profile.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)

        logger.error(
            f"[{agent_id}] JSON parse failed | "
            f"error={str(e)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "errors": {
                **state.get("errors", {}),
                agent_id: f"Failed to parse LLM response as JSON: {str(e)}",
            },
            "current_step": agent_id,
            "skill_profile": SkillProfile(
                skill_name="General Craft",
                skill_category="Handicrafts",
                experience_level="intermediate",
                sellable_products=["handmade items"],
                confidence_score=0.3,
            ).model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)

        logger.error(
            f"[{agent_id}] FAILED | "
            f"error={str(e)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "errors": {
                **state.get("errors", {}),
                agent_id: str(e),
            },
            "current_step": agent_id,
            "skill_profile": SkillProfile(
                skill_name="General Craft",
                skill_category="Handicrafts",
                experience_level="intermediate",
                sellable_products=["handmade items"],
                confidence_score=0.3,
            ).model_dump(),
        }