"""Shared LangChain helpers for LLM-backed agents."""

from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential

from config import settings


def build_chat_model(temperature: float = 0.2) -> ChatOpenAI:
    """Create the shared ChatOpenAI client used by LangChain agents."""
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        api_key=settings.OPENAI_API_KEY,
        temperature=temperature,
    )


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8), reraise=True)
def invoke_with_retry(chain: Any, payload: dict) -> Any:
    """Invoke a LangChain runnable with retry for transient model/network failures."""
    return chain.invoke(payload)
