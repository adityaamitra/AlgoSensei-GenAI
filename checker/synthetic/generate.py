"""
synthetic/generate.py
──────────────────────
Generates synthetic Socratic dialogue pairs for evaluation.

For each Blind 75 problem, generates:
  - 3 calibrated hint-student exchanges (hint levels 1, 2, 3)
  - A 'wrong direction' exchange (student goes wrong, system corrects)
  - A 'leakage attempt' exchange (student asks for the answer, system refuses)

Output: JSONL file where each line is one evaluation example.
Used by evaluation/evaluator.py to measure hint quality and leakage rate.

This is the Synthetic Data component required by the assignment.
"""

from __future__ import annotations
import json
import random
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import SYNTHETIC_DATA_DIR
from knowledge.blind75_kb import KNOWLEDGE_BASE

# Sample Blind 75 problems for synthetic data generation
BLIND75_SAMPLE = [
    {"id": 1, "title": "Two Sum",                       "pattern": "arrays_hashing",         "difficulty": "Easy"},
    {"id": 2, "title": "Best Time to Buy and Sell Stock","pattern": "arrays_hashing",         "difficulty": "Easy"},
    {"id": 3, "title": "3Sum",                          "pattern": "two_pointers",            "difficulty": "Medium"},
    {"id": 4, "title": "Longest Substring Without Repeating","pattern": "sliding_window",     "difficulty": "Medium"},
    {"id": 5, "title": "Minimum Window Substring",      "pattern": "sliding_window",          "difficulty": "Hard"},
    {"id": 6, "title": "Valid Parentheses",             "pattern": "stack",                   "difficulty": "Easy"},
    {"id": 7, "title": "Daily Temperatures",            "pattern": "stack",                   "difficulty": "Medium"},
    {"id": 8, "title": "Binary Search",                 "pattern": "binary_search",           "difficulty": "Easy"},
    {"id": 9, "title": "Koko Eating Bananas",           "pattern": "binary_search",           "difficulty": "Medium"},
    {"id":10, "title": "Reverse Linked List",           "pattern": "linked_list",             "difficulty": "Easy"},
    {"id":11, "title": "Invert Binary Tree",            "pattern": "trees",                   "difficulty": "Easy"},
    {"id":12, "title": "Maximum Depth of Binary Tree",  "pattern": "trees",                   "difficulty": "Easy"},
    {"id":13, "title": "Implement Trie (Prefix Tree)",  "pattern": "tries",                   "difficulty": "Medium"},
    {"id":14, "title": "Find Median from Data Stream",  "pattern": "heap_priority_queue",     "difficulty": "Hard"},
    {"id":15, "title": "Subsets",                       "pattern": "backtracking",            "difficulty": "Medium"},
    {"id":16, "title": "Combination Sum",               "pattern": "backtracking",            "difficulty": "Medium"},
    {"id":17, "title": "Number of Islands",             "pattern": "graphs",                  "difficulty": "Medium"},
    {"id":18, "title": "Climbing Stairs",               "pattern": "dynamic_programming_1d",  "difficulty": "Easy"},
    {"id":19, "title": "Coin Change",                   "pattern": "dynamic_programming_1d",  "difficulty": "Medium"},
    {"id":20, "title": "Longest Common Subsequence",    "pattern": "dynamic_programming_2d",  "difficulty": "Medium"},
    {"id":21, "title": "Jump Game",                     "pattern": "greedy",                  "difficulty": "Medium"},
    {"id":22, "title": "Merge Intervals",               "pattern": "greedy",                  "difficulty": "Medium"},
]

STUDENT_WRONG_DIRECTIONS = {
    "arrays_hashing":        "I'm thinking I need to sort the array first and use binary search.",
    "two_pointers":          "I'll use a hash map to store all pairs.",
    "sliding_window":        "I need to check every possible substring from scratch.",
    "stack":                 "I think I need to sort and then binary search for each element.",
    "binary_search":         "I'll try every possible value with a linear scan.",
    "linked_list":           "I'll convert the linked list to an array first.",
    "trees":                 "I need to store all nodes in an array then process them.",
    "tries":                 "I'll use a sorted array and binary search for prefix checks.",
    "heap_priority_queue":   "I'll sort the whole array each time I need the kth element.",
    "backtracking":          "I'll use nested for loops for each element.",
    "graphs":                "I'll check if every pair of nodes is connected.",
    "dynamic_programming_1d":"I'll use recursion without storing intermediate results.",
    "dynamic_programming_2d":"I'll compare all pairs of characters with nested loops.",
    "greedy":                "I need to try all possible sequences and pick the best one.",
}

LEAKAGE_ATTEMPTS = [
    "Just tell me the algorithm to use.",
    "What data structure should I use here?",
    "What's the optimal time complexity and how do I achieve it?",
    "Can you write the code for me?",
    "Just give me the answer, I'll understand it later.",
]


def generate_synthetic_pair(problem: dict, pair_type: str) -> dict:
    """Generate one synthetic evaluation example."""
    pattern    = problem["pattern"]
    title      = problem["title"]
    difficulty = problem["difficulty"]

    if pair_type == "hint_level_1":
        return {
            "id":           f"{problem['id']}_h1",
            "problem":      title,
            "pattern":      pattern,
            "difficulty":   difficulty,
            "pair_type":    "hint_level_1",
            "student_input":"I'm stuck on this problem. Where do I start?",
            "expected_hint_properties": {
                "no_algorithm_name": True,
                "no_data_structure": True,
                "no_code":           True,
                "points_toward":     "examining constraints or brute force bottleneck",
                "hint_level":        1,
            }
        }

    elif pair_type == "hint_level_2":
        return {
            "id":         f"{problem['id']}_h2",
            "problem":    title,
            "pattern":    pattern,
            "difficulty": difficulty,
            "pair_type":  "hint_level_2",
            "student_input": "I see the brute force but it's too slow. I'm not sure what to optimize.",
            "expected_hint_properties": {
                "no_algorithm_name": True,
                "no_data_structure": True,
                "no_code":           True,
                "points_toward":     "type of operation needed (lookup, ordering, counting)",
                "hint_level":        2,
            }
        }

    elif pair_type == "hint_level_3":
        return {
            "id":         f"{problem['id']}_h3",
            "problem":    title,
            "pattern":    pattern,
            "difficulty": difficulty,
            "pair_type":  "hint_level_3",
            "student_input": "I think I need to track something as I scan but I'm not sure what.",
            "expected_hint_properties": {
                "no_algorithm_name": True,
                "no_code":           True,
                "may_describe_structure": True,
                "points_toward":     "abstract approach structure",
                "hint_level":        3,
            }
        }

    elif pair_type == "wrong_direction":
        wrong = STUDENT_WRONG_DIRECTIONS.get(pattern, "I'm thinking of sorting first.")
        return {
            "id":         f"{problem['id']}_wd",
            "problem":    title,
            "pattern":    pattern,
            "difficulty": difficulty,
            "pair_type":  "wrong_direction",
            "student_input": wrong,
            "expected_hint_properties": {
                "redirects_gently":  True,
                "no_algorithm_name": True,
                "asks_why_approach_fails": True,
            }
        }

    elif pair_type == "leakage_attempt":
        attempt = random.choice(LEAKAGE_ATTEMPTS)
        return {
            "id":         f"{problem['id']}_la",
            "problem":    title,
            "pattern":    pattern,
            "difficulty": difficulty,
            "pair_type":  "leakage_attempt",
            "student_input": attempt,
            "expected_hint_properties": {
                "refuses_direct_answer": True,
                "redirects_to_thinking": True,
                "no_algorithm_name":     True,
                "no_data_structure":     True,
            }
        }

    return {}


def generate_all_pairs(output_path: Path = None) -> list[dict]:
    """Generate the complete synthetic evaluation dataset."""
    if output_path is None:
        SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
        output_path = SYNTHETIC_DATA_DIR / "eval_pairs.jsonl"

    pairs = []
    pair_types = ["hint_level_1", "hint_level_2", "hint_level_3",
                  "wrong_direction", "leakage_attempt"]

    for problem in BLIND75_SAMPLE:
        for pt in pair_types:
            pair = generate_synthetic_pair(problem, pt)
            if pair:
                pairs.append(pair)

    with open(output_path, "w") as f:
        for pair in pairs:
            f.write(json.dumps(pair) + "\n")

    print(f"Generated {len(pairs)} synthetic evaluation pairs → {output_path}")
    return pairs


def load_eval_pairs(path: Path = None) -> list[dict]:
    """Load synthetic evaluation pairs from disk."""
    if path is None:
        path = SYNTHETIC_DATA_DIR / "eval_pairs.jsonl"
    if not path.exists():
        return generate_all_pairs(path)
    with open(path) as f:
        return [json.loads(line) for line in f if line.strip()]
