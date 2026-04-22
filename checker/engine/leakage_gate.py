"""
engine/leakage_gate.py
Two-stage hint safety checker.
Stage 1: Fast regex (zero API cost, ~90% coverage)
Stage 2: Gemini semantic check
"""

from __future__ import annotations
import re, random
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

ALGORITHM_NAMES = [
    r"\bkadane\b", r"\bfloyd\b", r"\bdijkstra\b", r"\bbellman.ford\b",
    r"\bkruskal\b", r"\bprim\b", r"\bkmp\b", r"\brabin.karp\b",
    r"\bmanacher\b", r"\btopological\s+sort\b", r"\bunion.find\b", r"\bdisjoint\s+set\b",
]

DIRECT_DS_REVEALS = [
    r"use\s+a\s+hash\s+(map|table|set)",
    r"use\s+a\s+\w+\s+(stack|queue|heap|deque|trie)",
    r"monotonic\s+stack",
    r"use\s+a\s+(stack|queue|heap|deque|trie)",
    r"use\s+dynamic\s+programming",
    r"use\s+memoization",
    r"apply\s+memoization",
    r"you\s+need\s+a\s+(stack|queue|heap)",
    r"apply\s+(bfs|dfs|dp|greedy)",
    r"\bmemoization\b",
]

CODE_PATTERNS = [
    r"def\s+\w+\s*\(", r"for\s+\w+\s+in\s+", r"while\s+\w+",
    r"return\s+\w+", r"\.append\(", r"heapq\.", r"collections\.",
]

BIG_O_REVEALS = [
    r"o\(n\)\s+time", r"o\(1\)\s+space", r"o\(n\s+log\s+n\)",
    r"time\s+complexity\s+is\s+o", r"optimal\s+solution\s+is\s+o",
    r"optimal\s+time\s+complexity", r"the\s+optimal\s+(solution|approach)\s+is",
]


def rule_based_check(hint: str) -> dict:
    lower = hint.lower()
    for p in ALGORITHM_NAMES:
        if re.search(p, lower):
            return {"leaked": True, "reason": f"algorithm name: {p}", "severity": "high"}
    for p in DIRECT_DS_REVEALS:
        if re.search(p, lower):
            return {"leaked": True, "reason": f"ds reveal: {p}", "severity": "high"}
    for p in CODE_PATTERNS:
        if re.search(p, hint):
            return {"leaked": True, "reason": f"code syntax: {p}", "severity": "high"}
    for p in BIG_O_REVEALS:
        if re.search(p, lower):
            return {"leaked": True, "reason": f"complexity reveal: {p}", "severity": "low"}
    # Combo: dp + memoization in same hint
    if "dynamic programming" in lower and "memoization" in lower:
        return {"leaked": True, "reason": "dp+memoization combo", "severity": "high"}
    return {"leaked": False, "reason": None, "severity": "none"}


def semantic_check(hint: str) -> dict:
    from engine.gemini_client import generate_json
    from prompts.templates import LEAKAGE_CHECK_PROMPT
    try:
        result = generate_json(LEAKAGE_CHECK_PROMPT.format(hint=hint))
        return result if result else {"leaked": False, "reason": None, "severity": "none"}
    except Exception:
        return {"leaked": False, "reason": "check_failed", "severity": "none"}


def check_hint(hint: str, use_semantic: bool = True) -> dict:
    stage1 = rule_based_check(hint)
    if stage1["leaked"]:
        return {"safe": False, "stage": "rule_based",
                "reason": stage1["reason"], "severity": stage1["severity"]}
    if use_semantic:
        stage2 = semantic_check(hint)
        if stage2.get("leaked", False):
            return {"safe": False, "stage": "semantic",
                    "reason": stage2.get("reason"), "severity": stage2.get("severity", "low")}
    return {"safe": True, "stage": "passed", "reason": None, "severity": "none"}


SAFE_FALLBACKS = [
    "What's the simplest possible input? Trace through what needs to happen step by step.",
    "What information do you need to remember as you scan left to right?",
    "Write out the brute force first. Where exactly is the bottleneck?",
    "What do you know after processing the first element? The second? Is there a pattern?",
    "What's the relationship between consecutive elements that might be useful?",
]


def get_safe_fallback() -> str:
    return random.choice(SAFE_FALLBACKS)
