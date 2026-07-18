"""
Orchestrator — builds and executes the Meesho Udaan LangGraph pipeline.

This file owns the graph structure only. Zero business logic.

Parallel execution design:
  skill → [market, trend] → strategy → [pricing, branding, listing] → growth → compiler

LangGraph handles fan-out and fan-in automatically when multiple edges
point from one node or converge into one node.
"""

import logging
import uuid
from datetime import datetime
from typing import Any

from langgraph.graph import StateGraph, START, END

from app.agents.state import UdaanState, create_initial_state

# ── Agent node imports ────────────────────────────────────────────────────────
# Only the run function is imported from each agent.
# The orchestrator knows nothing about prompts, schemas, or LLM calls.

from app.agents.skill.agent import run as run_skill
from app.agents.market.agent import run as run_market
from app.agents.trend.agent import run as run_trend
from app.agents.strategy.agent import run as run_strategy
from app.agents.pricing.agent import run as run_pricing
from app.agents.branding.agent import run as run_branding
from app.agents.listing.agent import run as run_listing
from app.agents.growth.agent import run as run_growth
from app.agents.compiler.agent import run as run_compiler

logger = logging.getLogger(__name__)


# ─── Graph Builder ────────────────────────────────────────────────────────────


def build_graph() -> Any:
    """
    Constructs and compiles the LangGraph StateGraph.

    Uses UdaanState (TypedDict) as the state schema so LangGraph
    can correctly apply Annotated reducers during parallel execution.

    The compiled graph is stateless — safe to reuse across all requests.
    Each request provides its own initial state dict.
    """
    graph = StateGraph(UdaanState)

    # ── Register nodes ────────────────────────────────────────────────────────
    graph.add_node("skill_agent", run_skill)
    graph.add_node("market_agent", run_market)
    graph.add_node("trend_agent", run_trend)
    graph.add_node("strategy_agent", run_strategy)
    graph.add_node("pricing_agent", run_pricing)
    graph.add_node("branding_agent", run_branding)
    graph.add_node("listing_agent", run_listing)
    graph.add_node("growth_agent", run_growth)
    graph.add_node("compiler_agent", run_compiler)

    # ── Register edges ────────────────────────────────────────────────────────

    # Entry point
    graph.add_edge(START, "skill_agent")

    # Fan-out: skill → market + trend in parallel
    graph.add_edge("skill_agent", "market_agent")
    graph.add_edge("skill_agent", "trend_agent")

    # Fan-in: market + trend → strategy (strategy waits for both)
    graph.add_edge("market_agent", "strategy_agent")
    graph.add_edge("trend_agent", "strategy_agent")

    # Fan-out: strategy → pricing + branding + listing in parallel
    graph.add_edge("strategy_agent", "pricing_agent")
    graph.add_edge("strategy_agent", "branding_agent")
    graph.add_edge("strategy_agent", "listing_agent")

    # Fan-in: pricing + branding + listing → growth (growth waits for all three)
    graph.add_edge("pricing_agent", "growth_agent")
    graph.add_edge("branding_agent", "growth_agent")
    graph.add_edge("listing_agent", "growth_agent")

    # Final assembly and exit
    graph.add_edge("growth_agent", "compiler_agent")
    graph.add_edge("compiler_agent", END)

    return graph.compile()


# ── Compiled graph — built once at import time, reused for every request ──────
_graph = build_graph()


# ─── Public API ───────────────────────────────────────────────────────────────


async def run_pipeline(
    skill_text: str | None = None,
    skill_image_url: str | None = None,
    skill_audio_url: str | None = None,
    language: str = "en",
) -> dict[str, Any]:
    """
    Runs the full agent pipeline for a single user request.

    Creates a fresh state, invokes the compiled graph, and returns
    the final state dict for the API route to serialize and save.

    Args:
        skill_text:       Raw skill description from the user
        skill_image_url:  Optional Cloudinary URL of uploaded skill image
        skill_audio_url:  Optional Cloudinary URL of uploaded voice recording
        language:         Input language — "en" or "hi"

    Returns:
        Final merged state dict containing the compiled business blueprint
        and all intermediate agent outputs.
    """
    session_id = str(uuid.uuid4())

    logger.info(
        f"[orchestrator] Pipeline START | "
        f"session={session_id} | "
        f"input={'text' if skill_text else 'image/audio'}"
    )

    initial_state = create_initial_state(
        session_id=session_id,
        skill_text=skill_text,
        skill_image_url=skill_image_url,
        skill_audio_url=skill_audio_url,
        language=language,
    )

    started_at = datetime.utcnow()

    try:
        # ainvoke runs the graph asynchronously
        # LangGraph applies reducers automatically when parallel branches merge
        final_state: dict[str, Any] = await _graph.ainvoke(initial_state)

        duration_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)

        logger.info(
            f"[orchestrator] Pipeline COMPLETE | "
            f"session={session_id} | "
            f"duration={duration_ms}ms | "
            f"blueprint_id={final_state.get('blueprint_id', 'none')} | "
            f"errors={list(final_state.get('errors', {}).keys())}"
        )

        return final_state

    except Exception as e:
        duration_ms = int((datetime.utcnow() - started_at).total_seconds() * 1000)

        logger.error(
            f"[orchestrator] Pipeline FAILED | "
            f"session={session_id} | "
            f"duration={duration_ms}ms | "
            f"error={str(e)}"
        )

        # Return a safe failure state so the API can respond gracefully
        # rather than raising a 500 with no information
        failure_state = dict(initial_state)
        failure_state["errors"] = {"orchestrator": str(e)}
        failure_state["blueprint_ready"] = False
        failure_state["current_step"] = "failed"
        return failure_state