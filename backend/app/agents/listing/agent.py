"""
Listing Generation Agent.

Input:  business_strategy, brand_identity, pricing_strategy
Output: listing_content
"""

import json
import logging
import time

from app.agents.listing.prompt import SYSTEM_PROMPT, build_user_prompt
from app.agents.listing.schemas import ListingContent
from app.services.llm import get_llm

logger = logging.getLogger(__name__)

_FALLBACK = ListingContent(
    title="Handmade Indian Craft Product | Authentic Artisan Made | Premium Quality",
    description="Discover the beauty of authentic Indian craftsmanship.\n\n✅ Handmade by skilled artisans\n✅ Premium quality materials\n✅ Perfect for gifting and daily use\n✅ Unique — no two pieces identical",
    keywords=["handmade", "indian craft", "artisan", "ethnic", "traditional", "handcrafted", "gift", "authentic"],
    hindi_title="हस्तनिर्मित भारतीय शिल्प उत्पाद | प्रामाणिक कारीगर निर्मित",
    hindi_description="भारतीय कारीगरी की खूबसूरती को अनुभव करें। हस्तनिर्मित और प्रीमियम गुणवत्ता।",
    category_path="Handicrafts > Handmade Products",
)


def run(state: dict) -> dict:
    agent_id = "listing_agent"
    session_id = state.get("session_id", "unknown")
    started_at = time.time()

    logger.info(f"[{agent_id}] START | session={session_id}")

    business_strategy = state.get("business_strategy") or {}
    brand_identity = state.get("brand_identity") or {}
    pricing_strategy = state.get("pricing_strategy") or {}

    try:
        llm = get_llm(temperature=0.7)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": build_user_prompt(
                    business_strategy, brand_identity, pricing_strategy
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
        listing_content = ListingContent(**parsed)

        duration_ms = int((time.time() - started_at) * 1000)
        logger.info(
            f"[{agent_id}] COMPLETE | "
            f"session={session_id} | "
            f"title_length={len(listing_content.title)} | "
            f"keywords={len(listing_content.keywords)} | "
            f"duration={duration_ms}ms"
        )

        return {
            "listing_content": listing_content.model_dump(),
            "current_step": agent_id,
        }

    except json.JSONDecodeError as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] JSON parse failed | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: f"JSON parse error: {str(e)}"},
            "current_step": agent_id,
            "listing_content": _FALLBACK.model_dump(),
        }

    except Exception as e:
        duration_ms = int((time.time() - started_at) * 1000)
        logger.error(f"[{agent_id}] FAILED | {str(e)} | duration={duration_ms}ms")
        return {
            "errors": {**state.get("errors", {}), agent_id: str(e)},
            "current_step": agent_id,
            "listing_content": _FALLBACK.model_dump(),
        }