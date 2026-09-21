"""
ClaimLens Nexus — Ask ClaimLens Router (FR-004)

Natural-language question interface over the insurance data.
Per ADR-004: answers are always badged INSIGHT, never DECISION.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class AskRequest(BaseModel):
    question: str


@router.post("/ask")
async def ask_claimlens(request: AskRequest):
    """
    Ask a natural-language question about the insurance data.

    Pipeline: router → planner → SQL writer → guard → verifier → narrator
    Fallback: Groq → Gemini → cache → static template / golden queries

    Per ADR-004: the response is always an INSIGHT, never a DECISION.
    """
    from app.agent.chain import run_agent_chain

    result = await run_agent_chain(request.question)
    return result
