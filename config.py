"""
config.py
──────────
Central configuration.

Works in two environments:
  Local:      reads from .env file via python-dotenv
  HF Spaces:  reads from Spaces secrets (set in Settings → Secrets)

Required secrets:
  GEMINI_API_KEY   — from aistudio.google.com (free)
  QDRANT_URL       — from cloud.qdrant.io (free)
  QDRANT_API_KEY   — from cloud.qdrant.io (free)
"""

import os

# Try loading .env for local development; silently skip on HF Spaces
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ── API Keys ──────────────────────────────────────────────────
GEMINI_API_KEY  = os.environ.get("GEMINI_API_KEY", "")
QDRANT_URL      = os.environ.get("QDRANT_URL", "")
QDRANT_API_KEY  = os.environ.get("QDRANT_API_KEY", "")

# ── Qdrant ────────────────────────────────────────────────────
COLLECTION_NAME = "algosensei_knowledge"
EMBEDDING_DIM   = 384
TOP_K           = 4

# ── Models ────────────────────────────────────────────────────
EMBEDDING_MODEL      = "sentence-transformers/all-MiniLM-L6-v2"
GEMINI_MODEL         = "gemini-1.5-flash"
GEMINI_VISION_MODEL  = "gemini-1.5-flash"
MAX_OUTPUT_TOKENS    = 1024
TEMPERATURE          = 0.3

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
