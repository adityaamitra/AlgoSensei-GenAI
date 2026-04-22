"""
rag/embedder.py
────────────────
Pre-computes and caches embeddings for the entire knowledge base locally.
On first run: downloads all-MiniLM-L6-v2, embeds all chunks, saves to disk.
On subsequent runs: loads from cache instantly. Zero runtime cost per query.

This follows the proposal's commitment to a fully free stack:
embeddings are pre-computed once, not called via API on every request.
"""

from __future__ import annotations
import json
import os
import numpy as np
from pathlib import Path
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(x, **kw): return x

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import EMBEDDING_MODEL, EMBEDDINGS_CACHE, METADATA_CACHE
from knowledge.blind75_kb import get_all_chunks


def get_embedder():
    """Load the sentence transformer model (cached by HuggingFace locally)."""
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_knowledge_base(force: bool = False) -> tuple[np.ndarray, list[dict]]:
    """
    Embed all knowledge base chunks and cache to disk.

    Returns:
        embeddings: (N, 384) float32 numpy array
        metadata:   list of chunk dicts with id, pattern, topic, text
    """
    EMBEDDINGS_CACHE.parent.mkdir(parents=True, exist_ok=True)

    if not force and EMBEDDINGS_CACHE.exists() and METADATA_CACHE.exists():
        print("Loading embeddings from cache...")
        embeddings = np.load(str(EMBEDDINGS_CACHE))
        with open(METADATA_CACHE) as f:
            metadata = json.load(f)
        print(f"  Loaded {len(metadata)} chunks from cache.")
        return embeddings, metadata

    print(f"Computing embeddings for knowledge base...")
    chunks = get_all_chunks()
    model  = get_embedder()

    texts = [c["text"] for c in chunks]
    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        batch_size=32,
        normalize_embeddings=True,
    )

    np.save(str(EMBEDDINGS_CACHE), embeddings.astype(np.float32))
    with open(METADATA_CACHE, "w") as f:
        json.dump(chunks, f, indent=2)

    print(f"  Embedded {len(chunks)} chunks → saved to cache.")
    return embeddings.astype(np.float32), chunks


def embed_query(query: str) -> np.ndarray:
    """Embed a single query string for retrieval."""
    model = get_embedder()
    vec = model.encode([query], normalize_embeddings=True)
    return vec[0].astype(np.float32)
