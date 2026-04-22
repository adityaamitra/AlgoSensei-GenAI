"""
scripts/setup_qdrant.py
────────────────────────
Run this ONCE to set up AlgoSensei's knowledge base in Qdrant Cloud.

Steps:
  1. Embed all knowledge base chunks using all-MiniLM-L6-v2 (local, free)
  2. Create Qdrant collection if it doesn't exist
  3. Upload all embeddings with metadata
  4. Validate retrieval on a few test queries

Usage:
  python scripts/setup_qdrant.py
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import QDRANT_URL, QDRANT_API_KEY, COLLECTION_NAME
from rag.embedder import embed_knowledge_base
from rag.vector_store import (
    get_qdrant_client, create_collection_if_needed,
    upsert_knowledge_base, get_collection_stats
)
from rag.retriever import retrieve


def main():
    print("=" * 55)
    print("  AlgoSensei — Knowledge Base Setup")
    print("=" * 55)

    # Validate config
    if not QDRANT_URL or not QDRANT_API_KEY:
        print("\n✗ Missing Qdrant credentials.")
        print("  Set QDRANT_URL and QDRANT_API_KEY in your .env file.")
        print("  Get them free at: https://cloud.qdrant.io")
        sys.exit(1)

    print(f"\nQdrant URL:    {QDRANT_URL[:40]}...")
    print(f"Collection:    {COLLECTION_NAME}")

    # Step 1: Embed knowledge base
    print("\n[1/4] Computing embeddings (cached after first run)...")
    embeddings, metadata = embed_knowledge_base()
    print(f"      {len(metadata)} chunks, {embeddings.shape[1]}-dim vectors")

    # Step 2: Connect to Qdrant
    print("\n[2/4] Connecting to Qdrant Cloud...")
    client = get_qdrant_client()
    print("      Connected.")

    # Step 3: Create collection
    print("\n[3/4] Creating collection...")
    create_collection_if_needed(client)

    # Step 4: Upload
    print("\n[4/4] Uploading vectors...")
    upsert_knowledge_base(client, embeddings, metadata)

    # Validate
    print("\n── Validation ──────────────────────────────────────")
    stats = get_collection_stats()
    print(f"  Vectors in collection: {stats['vectors_count']}")
    print(f"  Collection status:     {stats['status']}")

    print("\n  Testing retrieval...")
    test_queries = [
        ("Two Sum complement lookup",     "arrays_hashing"),
        ("sliding window variable size",  "sliding_window"),
        ("monotonic stack next greater",  "stack"),
        ("DP recurrence relation coins",  "dynamic_programming_1d"),
    ]
    all_pass = True
    for query, expected_pattern in test_queries:
        results = retrieve(query, top_k=3)
        found   = any(r["pattern"] == expected_pattern for r in results)
        status  = "✓" if found else "✗"
        if not found:
            all_pass = False
        print(f"  {status} '{query}' → expected: {expected_pattern}, "
              f"got: {[r['pattern'] for r in results[:2]]}")

    print()
    if all_pass:
        print("✓ Setup complete. All retrieval tests passed.")
        print("\nNext step: streamlit run app.py")
    else:
        print("⚠ Setup complete but some retrieval tests failed.")
        print("  This may resolve after a few seconds as Qdrant indexes.")


if __name__ == "__main__":
    main()
