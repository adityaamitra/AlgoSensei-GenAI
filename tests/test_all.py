"""
tests/test_all.py
──────────────────
Test suite for AlgoSensei GenAI components.
Run: pytest tests/test_all.py -v

Tests cover:
  - Knowledge base structure and completeness
  - Embedding pipeline
  - Leakage gate (rule-based)
  - Retrieval faithfulness checker
  - Prompt template rendering
  - Synthetic data generation
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ── 1. Knowledge Base ─────────────────────────────────────────

class TestKnowledgeBase:

    def test_all_14_patterns_covered(self):
        from knowledge.blind75_kb import get_patterns
        patterns = get_patterns()
        assert len(patterns) >= 14, f"Expected 14 patterns, got {len(patterns)}"

    def test_minimum_chunk_count(self):
        from knowledge.blind75_kb import get_all_chunks
        chunks = get_all_chunks()
        assert len(chunks) >= 30, f"Expected ≥30 chunks, got {len(chunks)}"

    def test_all_chunks_have_required_fields(self):
        from knowledge.blind75_kb import get_all_chunks
        for chunk in get_all_chunks():
            assert "id"      in chunk, f"Missing id in chunk"
            assert "pattern" in chunk, f"Missing pattern in {chunk.get('id')}"
            assert "topic"   in chunk, f"Missing topic in {chunk.get('id')}"
            assert "text"    in chunk, f"Missing text in {chunk.get('id')}"
            assert len(chunk["text"]) > 50, f"Text too short in {chunk.get('id')}"

    def test_no_duplicate_chunk_ids(self):
        from knowledge.blind75_kb import get_all_chunks
        ids = [c["id"] for c in get_all_chunks()]
        assert len(ids) == len(set(ids)), "Duplicate chunk IDs found"

    def test_dp_patterns_present(self):
        from knowledge.blind75_kb import get_patterns
        patterns = get_patterns()
        assert "dynamic_programming_1d"  in patterns
        assert "dynamic_programming_2d" in patterns

    def test_get_chunks_by_pattern(self):
        from knowledge.blind75_kb import get_chunks_by_pattern
        chunks = get_chunks_by_pattern("trees")
        assert len(chunks) >= 2, "Trees pattern should have ≥2 chunks"


# ── 2. Leakage Gate ───────────────────────────────────────────

class TestLeakageGate:

    LEAKED = [
        "Use Kadane's algorithm here.",
        "You should use a hash map to store the complement.",
        "Apply dynamic programming with memoization.",
        "Use a monotonic stack to track the next greater element.",
        "def solution(nums): return sorted(nums)",
        "The optimal time complexity is O(n) time.",
    ]

    CLEAN = [
        "What do you notice about elements you've already scanned?",
        "Think about what information would help you avoid checking everything twice.",
        "If you solved this for just 2 elements, what would you do?",
        "What happens when you encounter a duplicate — what needs to change?",
        "Consider the brute force: where is it doing redundant work?",
    ]

    def test_leaked_hints_detected(self):
        from engine.leakage_gate import rule_based_check
        for hint in self.LEAKED:
            result = rule_based_check(hint)
            assert result["leaked"], f"Should flag as leaked: '{hint}'"

    def test_clean_hints_pass(self):
        from engine.leakage_gate import rule_based_check
        for hint in self.CLEAN:
            result = rule_based_check(hint)
            assert not result["leaked"], f"Should NOT flag: '{hint}'"

    def test_safe_fallbacks_pass(self):
        from engine.leakage_gate import SAFE_FALLBACKS, rule_based_check
        for fallback in SAFE_FALLBACKS:
            result = rule_based_check(fallback)
            assert not result["leaked"], f"Fallback should not be leaked: '{fallback}'"

    def test_check_hint_returns_required_fields(self):
        from engine.leakage_gate import check_hint
        result = check_hint("What do you notice?", use_semantic=False)
        assert "safe"     in result
        assert "stage"    in result
        assert "severity" in result

    def test_algorithm_name_patterns(self):
        from engine.leakage_gate import rule_based_check
        algorithms = [
            "Use Floyd's cycle detection.",
            "Apply Dijkstra's algorithm.",
            "Use the Union-Find data structure.",
        ]
        for hint in algorithms:
            result = rule_based_check(hint)
            assert result["leaked"], f"Should flag algorithm name: '{hint}'"


# ── 3. Prompt Templates ───────────────────────────────────────

class TestPromptTemplates:

    def test_explainer_prompt_renders(self):
        from prompts.templates import EXPLAINER_PROMPT
        rendered = EXPLAINER_PROMPT.format(
            topic="dynamic programming", context="[context]", pattern="dp_1d"
        )
        assert "dynamic programming" in rendered
        assert "[context]" in rendered

    def test_socratic_prompt_renders(self):
        from prompts.templates import SOCRATIC_HINT_PROMPT, HINT_LEVEL_GUIDANCE
        rendered = SOCRATIC_HINT_PROMPT.format(
            problem_title="Two Sum", difficulty="Easy",
            pattern="arrays_hashing", student_context="I'm stuck",
            context="[context]", hint_level=1,
            hint_level_guidance=HINT_LEVEL_GUIDANCE[1]
        )
        assert "Two Sum" in rendered
        assert "arrays_hashing" in rendered

    def test_hint_level_guidance_all_levels(self):
        from prompts.templates import HINT_LEVEL_GUIDANCE
        for level in [1, 2, 3]:
            assert level in HINT_LEVEL_GUIDANCE
            assert len(HINT_LEVEL_GUIDANCE[level]) > 20

    def test_screenshot_system_prompt_valid_json_instruction(self):
        from prompts.templates import SCREENSHOT_SYSTEM
        assert "problem_title" in SCREENSHOT_SYSTEM
        assert "pattern" in SCREENSHOT_SYSTEM
        assert "JSON" in SCREENSHOT_SYSTEM


# ── 4. Synthetic Data ─────────────────────────────────────────

class TestSyntheticData:

    def test_generate_pairs_all_types(self):
        from synthetic.generate import generate_synthetic_pair, BLIND75_SAMPLE
        problem    = BLIND75_SAMPLE[0]
        pair_types = ["hint_level_1", "hint_level_2", "hint_level_3",
                      "wrong_direction", "leakage_attempt"]
        for pt in pair_types:
            pair = generate_synthetic_pair(problem, pt)
            assert "id"           in pair, f"Missing id for type {pt}"
            assert "problem"      in pair, f"Missing problem for type {pt}"
            assert "pattern"      in pair, f"Missing pattern for type {pt}"
            assert "student_input" in pair, f"Missing student_input for type {pt}"

    def test_all_14_patterns_have_wrong_directions(self):
        from synthetic.generate import STUDENT_WRONG_DIRECTIONS
        from knowledge.blind75_kb import get_patterns
        for pat in get_patterns():
            if pat != "general":
                assert pat in STUDENT_WRONG_DIRECTIONS, f"Missing wrong direction for {pat}"

    def test_generate_pairs_count(self):
        import tempfile, json
        from pathlib import Path
        from synthetic.generate import generate_all_pairs
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False, mode="w") as f:
            tmp_path = Path(f.name)
        pairs = generate_all_pairs(tmp_path)
        assert len(pairs) >= 100, f"Expected ≥100 pairs, got {len(pairs)}"
        tmp_path.unlink()


# ── 5. Faithfulness Checker ───────────────────────────────────

class TestFaithfulness:

    def test_faithful_response_passes(self):
        from rag.retriever import check_retrieval_faithfulness
        chunks = [{"text": "hash map provides O(1) lookup by storing key value pairs"}]
        response = "Using a hash map provides O(1) lookup by storing key value pairs for fast access."
        result = check_retrieval_faithfulness(response, chunks)
        assert "faithful"  in result
        assert "coverage"  in result
        assert result["coverage"] >= 0.0

    def test_empty_chunks_returns_unfaithful(self):
        from rag.retriever import check_retrieval_faithfulness
        result = check_retrieval_faithfulness("some response", [])
        assert not result["faithful"]
        assert result["coverage"] == 0.0

    def test_faithfulness_coverage_bounded(self):
        from rag.retriever import check_retrieval_faithfulness
        chunks   = [{"text": "binary search eliminates half the search space"}]
        response = "This uses binary search to eliminate half the search space each step."
        result   = check_retrieval_faithfulness(response, chunks)
        assert 0.0 <= result["coverage"] <= 1.0


# ── 6. Tutor Session State ────────────────────────────────────

class TestTutoringSession:

    def test_session_initializes(self):
        from engine.tutor import TutoringSession
        s = TutoringSession()
        assert s.total_hints   == 0
        assert s.leakage_count == 0
        assert s.hint_level    == 0
        assert s.leakage_rate  == 0.0

    def test_leakage_rate_calculation(self):
        from engine.tutor import TutoringSession
        s = TutoringSession()
        s.total_hints   = 10
        s.leakage_count = 1
        assert abs(s.leakage_rate - 0.10) < 0.001

    def test_reset_problem(self):
        from engine.tutor import TutoringSession
        s = TutoringSession()
        s.current_problem = "Two Sum"
        s.hint_level = 2
        s.reset_problem()
        assert s.current_problem == ""
        assert s.hint_level == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
