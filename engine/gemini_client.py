"""
engine/gemini_client.py
────────────────────────
LLM client — supports both OpenAI and OpenRouter.

Switch provider in .env:
  LLM_PROVIDER=openai        → uses OPENAI_API_KEY + gpt-4o-mini
  LLM_PROVIDER=openrouter    → uses OPENROUTER_API_KEY + free models (default)

Both use the same OpenAI-compatible /v1/chat/completions endpoint.
No SDK needed — pure urllib.request HTTP calls.
"""

from __future__ import annotations
import json
import re
import base64
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    ACTIVE_API_KEY, ACTIVE_MODEL, ACTIVE_BASE_URL, ACTIVE_HEADERS,
    TEMPERATURE, MAX_OUTPUT_TOKENS,
    OPENROUTER_VISION_MODEL, OPENROUTER_API_KEY,
)


def _post(payload: dict, headers: dict = None) -> dict:
    import urllib.request, urllib.error
    h = headers or ACTIVE_HEADERS
    data = json.dumps(payload).encode()
    url  = f"{ACTIVE_BASE_URL}/chat/completions"
    req  = urllib.request.Request(url, data=data, headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"LLM API {e.code}: {body}") from e


def generate_text(prompt: str, system: str = "") -> str:
    """Generate a text response using the active provider/model."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    result = _post({
        "model":       ACTIVE_MODEL,
        "messages":    messages,
        "temperature": TEMPERATURE,
        "max_tokens":  MAX_OUTPUT_TOKENS,
    })
    return result["choices"][0]["message"]["content"].strip()


def generate_json(prompt: str, system: str = "") -> dict:
    """Generate a JSON response."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({
        "role": "user",
        "content": prompt + "\n\nRespond with valid JSON only, no markdown backticks."
    })

    result = _post({
        "model":       ACTIVE_MODEL,
        "messages":    messages,
        "temperature": 0.1,
        "max_tokens":  512,
    })
    text = result["choices"][0]["message"]["content"].strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def analyze_image(image_bytes: bytes, prompt: str, system: str = "") -> str:
    """
    Analyze an image using a vision-capable model.
    Always uses OpenRouter vision model regardless of active provider,
    since OpenAI vision requires a paid plan.
    """
    vision_headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/adityaamitra/AlgoSensei",
        "X-Title": "AlgoSensei",
        "Content-Type": "application/json",
    }
    vision_base = "https://openrouter.ai/api/v1"

    b64 = base64.b64encode(image_bytes).decode()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": [
        {"type": "text",      "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    ]})

    import urllib.request, urllib.error
    data = json.dumps({
        "model":       OPENROUTER_VISION_MODEL,
        "messages":    messages,
        "temperature": 0.1,
        "max_tokens":  512,
    }).encode()

    url = f"{vision_base}/chat/completions"
    req = urllib.request.Request(url, data=data, headers=vision_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise RuntimeError(f"Vision API error: {e}") from e