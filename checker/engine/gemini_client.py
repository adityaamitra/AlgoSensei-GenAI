"""
engine/gemini_client.py
────────────────────────
Thin wrapper around the Gemini API.
Handles text generation, vision (screenshot analysis), and JSON mode.
"""

from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Optional

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import GEMINI_API_KEY, GEMINI_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS


def get_model(system_instruction: str = ""):
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=system_instruction if system_instruction else None,
        generation_config={
            "temperature":     TEMPERATURE,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
        }
    )


def generate_text(prompt: str, system: str = "") -> str:
    """Generate a text response from Gemini."""
    model    = get_model(system)
    response = model.generate_content(prompt)
    return response.text.strip()


def generate_json(prompt: str, system: str = "") -> dict:
    """Generate a JSON response from Gemini. Strips markdown fences if present."""
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=system if system else None,
        generation_config={
            "temperature":       0.1,   # very low for structured output
            "max_output_tokens": 512,
            "response_mime_type": "application/json",
        }
    )
    response = model.generate_content(prompt)
    text = response.text.strip()
    # Strip markdown code fences if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}


def analyze_image(image_bytes: bytes, prompt: str, system: str = "") -> str:
    """Analyze an image with Gemini vision."""
    import google.generativeai as genai
    from PIL import Image
    import io
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL,
        system_instruction=system if system else None,
        generation_config={
            "temperature":       0.1,
            "max_output_tokens": 512,
            "response_mime_type": "application/json",
        }
    )
    image = Image.open(io.BytesIO(image_bytes))
    response = model.generate_content([prompt, image])
    return response.text.strip()
