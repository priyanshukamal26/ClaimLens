"""
ClaimLens Nexus — LLM Client with 4-Stage Fallback (ADR-003)

Fallback chain: Groq → Gemini → Cache → Static Template
Per AI_ML.md: free-tier rate limits are tight enough to exhaust mid-demo.
This fallback chain is load-bearing infrastructure, not a nice-to-have.

Per MASTER.md warning #2: Model IDs loaded from env vars, never hardcoded.
"""

import json
import hashlib
from typing import Optional
import httpx

from app.config import (
    GROQ_API_KEY, GROQ_MODEL_ID, GROQ_API_URL,
    GEMINI_API_KEY, GEMINI_MODEL_ID, GEMINI_API_URL,
)

# In-memory response cache
_response_cache: dict[str, str] = {}


async def call_llm(prompt: str, system_prompt: str = "") -> tuple[str, str]:
    """
    Call an LLM through the 4-stage fallback chain.

    Returns: (response_text, source) where source is one of:
    "groq", "gemini", "cache", "template"
    """
    # Check cache first (stage 3, but checked early for speed)
    cache_key = _cache_key(prompt)
    if cache_key in _response_cache:
        return _response_cache[cache_key], "cache"

    # Stage 1: Try Groq
    if GROQ_API_KEY and GROQ_MODEL_ID:
        try:
            result = await _call_groq(prompt, system_prompt)
            if result:
                _response_cache[cache_key] = result
                return result, "groq"
        except Exception as e:
            print(f"Groq failed: {e}")

    # Stage 2: Try Gemini
    if GEMINI_API_KEY and GEMINI_MODEL_ID:
        try:
            result = await _call_gemini(prompt, system_prompt)
            if result:
                _response_cache[cache_key] = result
                return result, "gemini"
        except Exception as e:
            print(f"Gemini failed: {e}")

    # Stage 3: Cache (already checked above)
    # Stage 4: Static template
    return "", "template"


async def _call_groq(prompt: str, system_prompt: str = "") -> Optional[str]:
    """Call Groq API."""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": GROQ_MODEL_ID,
                "messages": messages,
                "temperature": 0.1,
                "max_tokens": 1024,
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def _call_gemini(prompt: str, system_prompt: str = "") -> Optional[str]:
    """Call Gemini API."""
    full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            f"{GEMINI_API_URL}/models/{GEMINI_MODEL_ID}:generateContent?key={GEMINI_API_KEY}",
            json={
                "contents": [{"parts": [{"text": full_prompt}]}],
                "generationConfig": {
                    "temperature": 0.1,
                    "maxOutputTokens": 1024,
                },
            },
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]


def _cache_key(prompt: str) -> str:
    """Generate a cache key from a prompt."""
    return hashlib.md5(prompt.lower().strip().encode()).hexdigest()
