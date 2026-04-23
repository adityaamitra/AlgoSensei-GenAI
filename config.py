"""
config.py — AlgoSensei configuration
Works locally (.env file) and on HF Spaces (Secrets).
"""

import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── LLM Provider ──────────────────────────────────────────────
# Set LLM_PROVIDER="openai" in .env to use OpenAI (gpt-4o-mini)
# Leave unset or "openrouter" to use free OpenRouter models
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "openrouter")

# ── OpenAI ────────────────────────────────────────────────────
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL   = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# ── OpenRouter (free fallback) ────────────────────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL   = os.environ.get(
    "OPENROUTER_MODEL",
    "nvidia/llama-3.1-nemotron-ultra-253b-v1:free"
)
OPENROUTER_VISION_MODEL = os.environ.get(
    "OPENROUTER_VISION_MODEL",
    "qwen/qwen2-vl-7b-instruct:free"
)

# ── Active config (auto-resolved from provider) ───────────────
if LLM_PROVIDER == "openai" and OPENAI_API_KEY:
    ACTIVE_API_KEY  = OPENAI_API_KEY
    ACTIVE_MODEL    = OPENAI_MODEL
    ACTIVE_BASE_URL = "https://api.openai.com/v1"
    ACTIVE_HEADERS  = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
else:
    ACTIVE_API_KEY  = OPENROUTER_API_KEY
    ACTIVE_MODEL    = OPENROUTER_MODEL
    ACTIVE_BASE_URL = "https://openrouter.ai/api/v1"
    ACTIVE_HEADERS  = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/adityaamitra/AlgoSensei",
        "X-Title": "AlgoSensei",
        "Content-Type": "application/json",
    }

# Keep for backwards compatibility
GEMINI_API_KEY      = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL        = ACTIVE_MODEL
GEMINI_VISION_MODEL = OPENROUTER_VISION_MODEL

# ── Qdrant ────────────────────────────────────────────────────
QDRANT_URL      = os.environ.get("QDRANT_URL", "")
QDRANT_API_KEY  = os.environ.get("QDRANT_API_KEY", "")
COLLECTION_NAME = "algosensei_knowledge"
EMBEDDING_DIM   = 384
TOP_K           = 4

# ── Embedding model (local, free) ────────────────────────────
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ── Generation settings ───────────────────────────────────────
MAX_OUTPUT_TOKENS = 1024
TEMPERATURE       = 0.3

# ── Hint engine ───────────────────────────────────────────────
MAX_HINT_LEVELS   = 3
LEAKAGE_THRESHOLD = 0.05

# ── Chunking ──────────────────────────────────────────────────
CHUNK_SIZE    = 400
CHUNK_OVERLAP = 80

# ── Paths ─────────────────────────────────────────────────────
import pathlib
ROOT               = pathlib.Path(__file__).parent
EMBEDDINGS_CACHE   = ROOT / "rag" / "embeddings_cache.npy"
METADATA_CACHE     = ROOT / "rag" / "metadata_cache.json"
SYNTHETIC_DATA_DIR = ROOT / "synthetic" / "data"