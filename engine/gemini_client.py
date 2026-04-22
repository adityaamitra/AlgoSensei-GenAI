"""
engine/gemini_client.py
────────────────────────
Gemini API wrapper using the new google-genai SDK.

The old google-generativeai package is deprecated.
This uses: pip install google-genai
"""

from __future__ import annotations
import json
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS


def _client():
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def _config(temperature=None, max_tokens=None, json_mode=False):
    from google.genai import types
    kwargs = {
        "temperature":     temperature or TEMPERATURE,
        "max_output_tokens": max_tokens or MAX_OUTPUT_TOKENS,
    }
    if json_mode:
        kwargs["response_mime_type"] = "application/json"
    return types.GenerateContentConfig(**kwargs)


def generate_text(prompt: str, system: str = "") -> str:
    """Generate a text response from Gemini."""
    from google.genai import types
    client = _client()
    contents = []
    if system:
        contents.append(types.Content(
            role="user",
            parts=[types.Part(text=f"[System instruction: {system}]\n\n{prompt}")]
        ))
    else:
        contents.append(types.Content(
            role="user",
            parts=[types.Part(text=prompt)]
        ))
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=_config(),
    )
    return response.text.strip()


def generate_json(prompt: str, system: str = "") -> dict:
    """Generate a JSON response from Gemini."""
    from google.genai import types
    client = _client()
    full_prompt = f"[System: {system}]\n\n{prompt}" if system else prompt
    contents = [types.Content(role="user", parts=[types.Part(text=full_prompt)])]
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=_config(temperature=0.1, json_mode=True),
    )
    text = response.text.strip()
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def analyze_image(image_bytes: bytes, prompt: str, system: str = "") -> str:
    """Analyze an image with Gemini vision."""
    from google.genai import types
    from PIL import Image
    import io
    client = _client()
    image = Image.open(io.BytesIO(image_bytes))
    full_prompt = f"[System: {system}]\n\n{prompt}" if system else prompt
    contents = [
        types.Content(role="user", parts=[
            types.Part(text=full_prompt),
            types.Part(inline_data=types.Blob(
                mime_type="image/png",
                data=image_bytes
            ))
        ])
    ]
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=contents,
        config=_config(temperature=0.1, json_mode=True),
    )
    return response.text.strip()
