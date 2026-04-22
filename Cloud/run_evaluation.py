"""
scripts/run_evaluation.py
──────────────────────────
Standalone script to run the full AlgoSensei evaluation suite
and print a formatted report to stdout.

Usage:
    python scripts/run_evaluation.py
    python scripts/run_evaluation.py --save results/eval_report.json
"""

import sys, json, argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--save", type=str, default=None,
                        help="Path to save JSON report (optional)")
    args = parser.parse_args()

    print("=" * 55)
    print("  AlgoSensei — Evaluation Suite")
    print("=" * 55)

    from evaluation.evaluator import run_full_evaluation
    report = run_full_evaluation()

    print("\n── Full Report ─────────────────────────────────────")
    print(json.dumps(report, indent=2, default=str))

    if args.save:
        Path(args.save).parent.mkdir(parents=True, exist_ok=True)
        with open(args.save, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\nSaved: {args.save}")


if __name__ == "__main__":
    main()
