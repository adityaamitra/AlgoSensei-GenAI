"""
rag/vector_store.py
────────────────────
Qdrant Cloud vector store interface.

Handles:
  - Creating the collection if it doesn't exist
  - Upserting all knowledge base embeddings
  - Semantic search with metadata filtering
  - Retrieval faithfulness tracking
"""

from __future__ import annotations
import json
from pathlib import Path
from typing import Optional

import numpy as np

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import (
    QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME,
    EMBEDDING_DIM, TOP_K
)


def get_qdrant_client():
    from qdrant_client import QdrantClient
    return QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)


def create_collection_if_needed(client) -> None:
    """Create the Qdrant collection if it doesn't already exist."""
    from qdrant_client.models import Distance, VectorParams
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
        print(f"  Created collection: {COLLECTION_NAME}")
    else:
        print(f"  Collection already exists: {COLLECTION_NAME}")


def upsert_knowledge_base(
    client,
    embeddings: np.ndarray,
    metadata: list[dict]
) -> None:
    """Upload all embeddings with metadata to Qdrant."""
    from qdrant_client.models import PointStruct

    points = [
        PointStruct(
            id=i,
            vector=embeddings[i].tolist(),
            payload={
                "chunk_id": chunk["id"],
                "pattern":  chunk["pattern"],
                "topic":    chunk["topic"],
                "text":     chunk["text"],
            }
        )
        for i, chunk in enumerate(metadata)
    ]

    # Upsert in batches of 100
    batch_size = 100
    for start in range(0, len(points), batch_size):
        batch = points[start:start + batch_size]
        client.upsert(collection_name=COLLECTION_NAME, points=batch)

    print(f"  Upserted {len(points)} vectors to Qdrant.")


def search(
    query_vector: np.ndarray,
    top_k: int = TOP_K,
    pattern_filter: Optional[str] = None,
) -> list[dict]:
    """
    Semantic search over the knowledge base.
    Compatible with both qdrant-client <1.7 (client.search) and >=1.7 (client.query_points).
    """
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    client = get_qdrant_client()

    query_filter = None
    if pattern_filter:
        query_filter = Filter(
            must=[FieldCondition(
                key="pattern",
                match=MatchValue(value=pattern_filter)
            )]
        )

    # qdrant-client >=1.7 uses query_points(); older uses search()
    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector.tolist(),
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )
        results = response.points
    else:
        results = client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector.tolist(),
            limit=top_k,
            query_filter=query_filter,
            with_payload=True,
        )

    return [
        {
            "text":    r.payload["text"],
            "pattern": r.payload["pattern"],
            "topic":   r.payload["topic"],
            "chunk_id":r.payload["chunk_id"],
            "score":   round(r.score, 4),
        }
        for r in results
    ]


def get_collection_stats() -> dict:
    """Return basic stats about the collection."""
    client = get_qdrant_client()
    info = client.get_collection(COLLECTION_NAME)
    # qdrant-client >=1.7 uses points_count; older versions use vectors_count
    count = (getattr(info, "points_count", None)
             or getattr(info, "vectors_count", None)
             or "unknown")
    return {
        "vectors_count": count,
        "status":        str(info.status),
    }
