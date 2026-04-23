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

# ── OpenRouter (replaces Gemini direct API) ───────────────────
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")

# Confirmed working free models on OpenRouter:
#   "qwen/qwen-2.5-7b-instruct:free"       ← default, good for coding
#   "meta-llama/llama-3.1-8b-instruct:free"
#   "mistralai/mistral-7b-instruct:free"
#   "google/gemma-2-9b-it:free"
OPENROUTER_MODEL   = os.environ.get(
    "OPENROUTER_MODEL",
    "qwen/qwen-2.5-7b-instruct:free"
)

# Separate vision model for screenshot analysis (must support image input)
# meta-llama/llama-3.2-11b-vision-instruct:free supports images
OPENROUTER_VISION_MODEL = os.environ.get(
    "OPENROUTER_VISION_MODEL",
    "qwen/qwen2-vl-7b-instruct:free"
)

# Keep these for backwards compatibility
GEMINI_API_KEY      = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL        = OPENROUTER_MODEL
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
