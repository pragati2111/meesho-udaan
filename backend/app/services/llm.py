"""
LLM Service — centralized Gemini client for all AI agent calls.

All agents call get_llm() to get the configured Gemini client.
Changing the model/provider later requires modifying only this file.
"""

import logging
from functools import lru_cache

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_llm(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """
    Returns a cached Gemini client.

    Different temperatures can be used by different agents.

    Pricing Agent      -> 0.1
    Market Agent       -> 0.2
    Skill Agent        -> 0.3
    Branding Agent     -> 0.9
    """

    logger.info(f"Initializing Gemini client | temperature={temperature}")

    return ChatGoogleGenerativeAI(
       model="gemini-flash-latest",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=temperature,
    )


def get_precise_llm() -> ChatGoogleGenerativeAI:
    """Deterministic reasoning."""
    return get_llm(temperature=0.1)


def get_creative_llm() -> ChatGoogleGenerativeAI:
    """Creative generation."""
    return get_llm(temperature=0.9)