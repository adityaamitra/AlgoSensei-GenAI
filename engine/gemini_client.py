"""
engine/gemini_client.py
────────────────────────
LLM client — now using OpenRouter (OpenAI-compatible API).

OpenRouter gives access to many models including free ones.
Get your key at: https://openrouter.ai/keys

Free models that work well for this project:
  - google/gemini-2.0-flash-exp:free    (fast, good quality)
  - meta-llama/llama-3.1-8b-instruct:free
  - mistralai/mistral-7b-instruct:free

Set OPENROUTER_MODEL in config.py to switch models.
"""

from __future__ import annotations
import json
import re
import base64
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import OPENROUTER_API_KEY, OPENROUTER_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/adityaamitra/AlgoSensei",
        "X-Title": "AlgoSensei",
        "Content-Type": "application/json",
    }


def _post(payload: dict) -> dict:
    import urllib.request
    import urllib.error
    data = json.dumps(payload).encode()
    req  = urllib.request.Request(
        f"{OPENROUTER_BASE_URL}/chat/completions",
        data=data, headers=_headers(), method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"OpenRouter {e.code}: {body}") from e


def generate_text(prompt: str, system: str = "") -> str:
    """Generate a text response."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    result = _post({
        "model":       OPENROUTER_MODEL,
        "messages":    messages,
        "temperature": TEMPERATURE,
        "max_tokens":  MAX_OUTPUT_TOKENS,
    })
    return result["choices"][0]["message"]["content"].strip()


def generate_json(prompt: str, system: str = "") -> dict:
    """Generate a JSON response. Uses response_format for supported models."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user",
                     "content": prompt + "\n\nRespond with valid JSON only, no markdown."})

    result = _post({
        "model":       OPENROUTER_MODEL,
        "messages":    messages,
        "temperature": 0.1,
        "max_tokens":  512,
    })
    text = result["choices"][0]["message"]["content"].strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*",     "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def analyze_image(image_bytes: bytes, prompt: str, system: str = "") -> str:
    """Analyze an image — uses vision-capable model on OpenRouter."""
    b64 = base64.b64encode(image_bytes).decode()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": [
        {"type": "text",      "text": prompt + "\n\nRespond with valid JSON only."},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
    ]})

    result = _post({
        "model":      OPENROUTER_MODEL,
        "messages":   messages,
        "temperature": 0.1,
        "max_tokens":  512,
    })
    return result["choices"][0]["message"]["content"].strip()
