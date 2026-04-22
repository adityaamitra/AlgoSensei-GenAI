"""
engine/tutor.py
────────────────
The core AlgoSensei tutoring engine.

Three modes, one engine:
  - explainer:   concept grounding with retrieved citations
  - socratic:    calibrated hint generation with leakage gate
  - screenshot:  vision → pattern detection → socratic

All responses include:
  - retrieved_chunks:   what was retrieved from Qdrant
  - leakage_result:     safety check result
  - faithfulness:       how grounded in retrieved context
  - mode:               which mode was used
  - response:           the actual text shown to student
"""

from __future__ import annotations
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from rag.retriever import retrieve, format_context, check_retrieval_faithfulness
from engine.gemini_client import generate_text, generate_json, analyze_image
from engine.leakage_gate import check_hint, get_safe_fallback
from prompts.templates import (
    EXPLAINER_SYSTEM, EXPLAINER_PROMPT,
    SOCRATIC_SYSTEM, SOCRATIC_HINT_PROMPT, HINT_LEVEL_GUIDANCE,
    SCREENSHOT_SYSTEM, SCREENSHOT_FALLBACK,
    MODE_DETECTION_PROMPT,
)


class TutoringSession:
    """
    Maintains state for one student's tutoring session.
    Tracks hint levels, mode history, and interaction metrics.
    """

    def __init__(self):
        self.history:         list[dict] = []
        self.current_problem: str        = ""
        self.current_pattern: str        = ""
        self.hint_level:      int        = 0
        self.total_hints:     int        = 0
        self.leakage_count:   int        = 0
        self.mode_counts:     dict       = {"explainer": 0, "socratic": 0, "screenshot": 0}

    def reset_problem(self):
        self.current_problem = ""
        self.current_pattern = ""
        self.hint_level      = 0

    @property
    def leakage_rate(self) -> float:
        if self.total_hints == 0:
            return 0.0
        return self.leakage_count / self.total_hints


class AlgoSenseiEngine:
    """Main tutoring engine. Instantiate once per app session."""

    def __init__(self):
        self.session = TutoringSession()

    # ── Mode detection ────────────────────────────────────────

    def detect_mode(self, message: str, has_image: bool = False) -> dict:
        """Determine which mode to use based on student message."""
        if has_image:
            return {"mode": "screenshot", "topic": "screenshot problem"}
        prompt = MODE_DETECTION_PROMPT.format(
            message=message, has_image=has_image
        )
        result = generate_json(prompt)
        if not result or "mode" not in result:
            return {"mode": "socratic", "topic": message[:80]}
        return result

    # ── Mode 1: Explainer ─────────────────────────────────────

    def explain(self, topic: str, pattern: str = "") -> dict:
        """
        Explain a DSA concept with retrieved context and analogies.
        """
        self.session.mode_counts["explainer"] += 1
        query   = f"{topic} {pattern} concept explanation analogy"
        chunks  = retrieve(query, pattern_filter=pattern or None)
        context = format_context(chunks)

        prompt   = EXPLAINER_PROMPT.format(
            topic=topic, context=context, pattern=pattern or "general DSA"
        )
        response = generate_text(prompt, system=EXPLAINER_SYSTEM)
        faith    = check_retrieval_faithfulness(response, chunks)

        self.session.history.append({
            "mode": "explainer", "topic": topic, "response": response
        })

        return {
            "mode":              "explainer",
            "response":          response,
            "retrieved_chunks":  chunks,
            "faithfulness":      faith,
            "leakage_result":    {"safe": True, "stage": "passed"},
        }

    # ── Mode 2: Socratic ──────────────────────────────────────

    def hint(
        self,
        problem_title: str,
        difficulty:    str,
        pattern:       str,
        student_context: str = "",
        hint_level:    int   = None,
        max_retries:   int   = 3,
    ) -> dict:
        """
        Generate a Socratic hint at the given calibration level.
        Runs the leakage gate and retries if leaked.
        """
        self.session.mode_counts["socratic"] += 1
        self.session.current_problem = problem_title
        self.session.current_pattern = pattern

        if hint_level is None:
            self.session.hint_level = min(self.session.hint_level + 1, 3)
            hint_level = self.session.hint_level
        else:
            self.session.hint_level = hint_level

        query  = f"{problem_title} {pattern} hint approach key insight"
        chunks = retrieve(query, pattern_filter=pattern)
        context = format_context(chunks)

        guidance = HINT_LEVEL_GUIDANCE.get(hint_level, HINT_LEVEL_GUIDANCE[1])

        leakage_result = {"safe": False}
        response       = ""
        attempt        = 0

        while not leakage_result["safe"] and attempt < max_retries:
            attempt += 1
            prompt = SOCRATIC_HINT_PROMPT.format(
                problem_title=problem_title,
                difficulty=difficulty,
                pattern=pattern,
                student_context=student_context or "Not provided",
                context=context,
                hint_level=hint_level,
                hint_level_guidance=guidance,
            )
            response       = generate_text(prompt, system=SOCRATIC_SYSTEM)
            leakage_result = check_hint(response)

        self.session.total_hints += 1
        if not leakage_result["safe"]:
            self.session.leakage_count += 1
            response = get_safe_fallback()
            leakage_result = {"safe": True, "stage": "fallback",
                              "reason": "max retries exceeded — using fallback"}

        faith = check_retrieval_faithfulness(response, chunks)
        self.session.history.append({
            "mode": "socratic", "problem": problem_title,
            "hint_level": hint_level, "response": response
        })

        return {
            "mode":              "socratic",
            "response":          response,
            "hint_level":        hint_level,
            "retrieved_chunks":  chunks,
            "faithfulness":      faith,
            "leakage_result":    leakage_result,
            "session_hints":     self.session.total_hints,
            "leakage_rate":      round(self.session.leakage_rate, 4),
        }

    # ── Mode 3: Screenshot Solver ─────────────────────────────

    def analyze_screenshot(self, image_bytes: bytes) -> dict:
        """
        Use Gemini vision to identify the problem and pattern from a screenshot.
        Returns structured problem info + first direction hint.
        """
        self.session.mode_counts["screenshot"] += 1
        try:
            raw   = analyze_image(image_bytes, "Analyze this LeetCode problem screenshot.", SCREENSHOT_SYSTEM)
            # Strip markdown fences
            import re
            raw = re.sub(r"```json\s*", "", raw)
            raw = re.sub(r"```\s*", "", raw).strip()
            info  = json.loads(raw)
        except Exception as e:
            return {
                "mode":     "screenshot",
                "success":  False,
                "response": SCREENSHOT_FALLBACK,
                "error":    str(e),
            }

        # Update session with detected problem
        self.session.current_problem = info.get("problem_title", "Unknown")
        self.session.current_pattern = info.get("pattern", "")
        self.session.hint_level      = 0

        # Get first Socratic hint using the detected info
        first_hint = info.get("first_hint_direction", "")
        leakage    = check_hint(first_hint)
        if not leakage["safe"]:
            first_hint = get_safe_fallback()

        return {
            "mode":          "screenshot",
            "success":       True,
            "problem_title": info.get("problem_title", "Unknown"),
            "difficulty":    info.get("difficulty", "Unknown"),
            "pattern":       info.get("pattern", ""),
            "constraints":   info.get("key_constraints", []),
            "confidence":    info.get("pattern_confidence", "medium"),
            "response":      first_hint,
            "leakage_result": leakage,
        }

    # ── Respond (unified entry point) ─────────────────────────

    def respond(
        self,
        message:     str,
        image_bytes: bytes = None,
        problem:     str   = "",
        pattern:     str   = "",
        difficulty:  str   = "Medium",
        hint_level:  int   = None,
    ) -> dict:
        """
        Unified entry point. Detects mode and routes appropriately.
        """
        if image_bytes:
            return self.analyze_screenshot(image_bytes)

        mode_info = self.detect_mode(message, has_image=False)
        mode      = mode_info.get("mode", "socratic")

        if mode == "explainer":
            topic = mode_info.get("topic", message)
            return self.explain(topic, pattern=pattern)

        elif mode == "socratic":
            return self.hint(
                problem_title    = problem or self.session.current_problem or message[:50],
                difficulty       = difficulty,
                pattern          = pattern or self.session.current_pattern,
                student_context  = message,
                hint_level       = hint_level,
            )

        return self.explain(message, pattern=pattern)

    def get_session_stats(self) -> dict:
        return {
            "total_hints":    self.session.total_hints,
            "leakage_rate":   round(self.session.leakage_rate, 4),
            "leakage_count":  self.session.leakage_count,
            "mode_counts":    self.session.mode_counts,
            "current_problem":self.session.current_problem,
            "hint_level":     self.session.hint_level,
        }
