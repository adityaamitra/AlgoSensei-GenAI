"""
scripts/generate_synthetic.py
───────────────────────────────
Generate synthetic Socratic dialogue pairs for the evaluation suite.

Creates:
  synthetic/data/eval_pairs.jsonl   — 110 evaluation pairs
  synthetic/data/stats.json         — distribution summary

Usage:
    python scripts/generate_synthetic.py
"""

import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from synthetic.generate import generate_all_pairs, BLIND75_SAMPLE
from config import SYNTHETIC_DATA_DIR


def main():
    print("=" * 55)
    print("  AlgoSensei — Synthetic Data Generation")
    print("=" * 55)

    SYNTHETIC_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = SYNTHETIC_DATA_DIR / "eval_pairs.jsonl"

    print(f"\nProblems:    {len(BLIND75_SAMPLE)}")
    print(f"Types/prob:  5 (hint L1, L2, L3, wrong direction, leakage attempt)")
    print(f"Total pairs: {len(BLIND75_SAMPLE) * 5}")
    print(f"Output:      {output_path}")
    print()

    pairs = generate_all_pairs(output_path)

    # Stats
    from collections import Counter
    type_counts    = Counter(p["pair_type"] for p in pairs)
    pattern_counts = Counter(p["pattern"]   for p in pairs)

    stats = {
        "total_pairs":    len(pairs),
        "by_type":        dict(type_counts),
        "by_pattern":     dict(pattern_counts),
        "output_path":    str(output_path),
    }
    stats_path = SYNTHETIC_DATA_DIR / "stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    print("\n── Distribution ────────────────────────────────────")
    for pt, count in type_counts.items():
        print(f"  {pt:<25} {count:>4} pairs")
    print(f"\n  Total: {len(pairs)} pairs")
    print(f"\n✓ Done. Saved to: {output_path}")


if __name__ == "__main__":
    main()
