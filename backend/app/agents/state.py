"""
UdaanState — Shared state for the Meesho Udaan LangGraph pipeline.

Uses TypedDict (required by LangGraph StateGraph) instead of Pydantic BaseModel.
Fields updated by parallel agents use Annotated reducers to prevent merge conflicts.

Reducer rules:
- errors: dict_merge reducer — parallel agents can each write their own key
- current_step: last_value reducer — we keep the most recent step name
- All other fields: default reducer (last write wins) — each agent owns its section
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any
from typing_extensions import TypedDict
import operator


# ─── Reducer Functions ────────────────────────────────────────────────────────


def dict_merge(left: dict, right: dict) -> dict:
    """
    Merges two dicts by combining their keys.
    Used for the errors field so parallel agents can each add their own error
    without overwriting what another parallel agent wrote.
    """
    merged = {**left}
    merged.update(right)
    return merged


def last_value(left: Any, right: Any) -> Any:
    """
    Returns the most recently written value.
    Used for current_step — we always want the latest agent name.
    """
    return right if right is not None else left


def list_concat(left: list, right: list) -> list:
    """
    Concatenates two lists.
    Used for warnings so parallel agents can each append without overwriting.
    """
    return left + right


# ─── State Definition ─────────────────────────────────────────────────────────


class UdaanState(TypedDict, total=False):
    """
    Complete shared state flowing through every node in the LangGraph graph.

    total=False means all fields are optional at initialization —
    the graph starts with only the input fields set and agents fill in the rest.

    Fields used by parallel agents have Annotated reducers:
    - errors: dict_merge — both market_agent and trend_agent can write errors
    - warnings: list_concat — parallel agents can each append warnings
    - current_step: last_value — we always keep the most recent step name

    All other fields are owned exclusively by one agent (last write wins is safe).
    """

    # ── Input fields (set once at graph start) ────────────────────────────────
    session_id: str
    skill_text: str | None
    skill_image_url: str | None
    skill_audio_url: str | None
    language: str

    # ── Agent outputs (each owned by exactly one agent) ───────────────────────
    skill_profile: dict | None
    market_intelligence: dict | None
    trend_analysis: dict | None
    business_strategy: dict | None
    pricing_strategy: dict | None
    brand_identity: dict | None
    listing_content: dict | None
    growth_plan: dict | None

    # ── Compiler output ───────────────────────────────────────────────────────
    blueprint_id: str | None
    blueprint_ready: bool
    compiled_blueprint: dict | None

    # ── Execution metadata ────────────────────────────────────────────────────
    started_at: str                                         # ISO format datetime string
    completed_at: str | None

    # Annotated reducers for fields written by parallel agents
    errors: Annotated[dict, dict_merge]                     # agent_id -> error message
    warnings: Annotated[list, list_concat]                  # non-fatal notices
    current_step: Annotated[str, last_value]                # most recent agent name


# ─── State Factory ────────────────────────────────────────────────────────────


def create_initial_state(
    session_id: str,
    skill_text: str | None = None,
    skill_image_url: str | None = None,
    skill_audio_url: str | None = None,
    language: str = "en",
) -> UdaanState:
    """
    Creates a fresh state dict for a new pipeline run.

    Always use this factory — never construct UdaanState manually.
    This guarantees all Annotated reducer fields start as empty
    containers rather than None, which would break the reducers.
    """
    return UdaanState(
        session_id=session_id,
        skill_text=skill_text,
        skill_image_url=skill_image_url,
        skill_audio_url=skill_audio_url,
        language=language,
        skill_profile=None,
        market_intelligence=None,
        trend_analysis=None,
        business_strategy=None,
        pricing_strategy=None,
        brand_identity=None,
        listing_content=None,
        growth_plan=None,
        blueprint_id=None,
        blueprint_ready=False,
        compiled_blueprint=None,
        started_at=datetime.utcnow().isoformat(),
        completed_at=None,
        errors={},          # must be empty dict, not None — reducer requires a dict
        warnings=[],        # must be empty list, not None — reducer requires a list
        current_step="initializing",
    )