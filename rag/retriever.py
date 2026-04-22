"""
rag/retriever.py
─────────────────
Unified retrieval interface. The engine only talks to this module.

retrieve(query) → list of relevant chunks with citations
Each chunk has a 'source' field used for faithfulness scoring.
"""

from __future__ import annotations
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.embedder import embed_query
from rag.vector_store import search
from config import TOP_K


def retrieve(
    query: str,
    top_k: int = TOP_K,
    pattern_filter: str = None,
) -> list[dict]:
    """
    Retrieve the most relevant knowledge base chunks for a query.

    Returns list of dicts:
        text, pattern, topic, chunk_id, score, source (citation string)
    """
    vec     = embed_query(query)
    results = search(vec, top_k=top_k, pattern_filter=pattern_filter)

    for r in results:
        # Build a short citation string for the report
        pattern_display = r["pattern"].replace("_", " ").title()
        r["source"] = f"AlgoSensei KB — {pattern_display} ({r['topic']})"

    return results


def format_context(chunks: list[dict]) -> str:
    """
    Format retrieved chunks into a context block for Gemini prompts.
    Each chunk is numbered and sourced for faithfulness verification.
    """
    if not chunks:
        return "No relevant context retrieved."

    lines = []
    for i, chunk in enumerate(chunks, 1):
        lines.append(
            f"[{i}] Source: {chunk['source']} (relevance: {chunk['score']})\n"
            f"{chunk['text'].strip()}"
        )
    return "\n\n".join(lines)


def check_retrieval_faithfulness(response: str, chunks: list[dict]) -> dict:
    """
    Simple faithfulness check: does the response contain key terms
    from the retrieved chunks?

    Returns: {faithful: bool, coverage: float, missing_concepts: list}
    """
    if not chunks:
        return {"faithful": False, "coverage": 0.0, "missing_concepts": []}

    # Extract key technical terms from chunks
    all_chunk_text = " ".join(c["text"].lower() for c in chunks)
    response_lower = response.lower()

    # Key terms that should appear in both retrieved context and response
    technical_terms = [
        word for word in all_chunk_text.split()
        if len(word) > 5 and word.isalpha()
        and word not in {"which", "where", "their", "about", "every",
                         "these", "those", "using", "being", "since"}
    ]
    unique_terms = list(set(technical_terms))[:20]

    matched = [t for t in unique_terms if t in response_lower]
    coverage = len(matched) / len(unique_terms) if unique_terms else 1.0
    missing  = [t for t in unique_terms if t not in response_lower][:5]

    return {
        "faithful":        coverage >= 0.3,
        "coverage":        round(coverage, 3),
        "missing_concepts": missing,
    }
