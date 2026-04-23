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




def _extract_text_from_image(image_bytes: bytes) -> str:
    """
    Extract text from image using pytesseract (local OCR).
    Falls back to vision API if tesseract not installed.
    """
    from PIL import Image
    import io

    # Try pytesseract first (local, free, no API needed)
    try:
        import pytesseract
        image = Image.open(io.BytesIO(image_bytes))
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        text = pytesseract.image_to_string(image)
        if text and len(text.strip()) > 20:
            return text.strip()
    except (ImportError, Exception):
        pass

    # Fall back to vision API
    try:
        vision_prompt = (
            "Read this LeetCode problem screenshot. "
            "Extract the problem title, difficulty, and description as plain text."
        )
        return analyze_image(image_bytes, vision_prompt, "")
    except Exception as e:
        return ""


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
        Two-step screenshot analysis:
        Step 1: Vision model reads raw text from image
        Step 2: Text model extracts structured info + first hint
        """
        self.session.mode_counts["screenshot"] += 1

        # Extract text from image using pytesseract if available,
        # otherwise fall back to vision API
        raw_text = _extract_text_from_image(image_bytes)
        if not raw_text or len(raw_text) < 20:
            return {
                "mode": "screenshot", "success": False,
                "response": SCREENSHOT_FALLBACK,
                "error": "Could not extract text from image. Try the Get a Hint tab instead.",
            }

        extract_prompt = (
            "Given this text from a LeetCode screenshot:\n\n"
            + raw_text
            + "\n\nReturn ONLY valid JSON with these exact keys:\n"
            + '{"problem_title":"name","difficulty":"Easy|Medium|Hard",'
            + '"pattern":"arrays_hashing|two_pointers|sliding_window|stack|binary_search|linked_list|trees|tries|heap_priority_queue|backtracking|graphs|dynamic_programming_1d|dynamic_programming_2d|greedy",'
            + '"key_constraints":["c1","c2"],'
            + '"pattern_confidence":"high|medium|low",'
            + '"first_hint_direction":"one sentence hint without naming the algorithm"}'
        )

        try:
            info = generate_json(extract_prompt)
        except Exception:
            info = {}

        if not info or "problem_title" not in info:
            title = "Unknown Problem"
            for line in raw_text.splitlines():
                line = line.strip().lstrip("0123456789. ")
                if line and 3 < len(line) < 60:
                    title = line
                    break
            info = {
                "problem_title": title,
                "difficulty": "Medium",
                "pattern": "arrays_hashing",
                "key_constraints": [],
                "pattern_confidence": "low",
                "first_hint_direction": (
                    "What do you notice about the input and what the problem is asking you to find?"
                ),
            }

        self.session.current_problem = info.get("problem_title", "Unknown")
        self.session.current_pattern = info.get("pattern", "")
        self.session.hint_level      = 0

        first_hint = info.get("first_hint_direction") or get_safe_fallback()
        leakage    = check_hint(first_hint, use_semantic=False)
        if not leakage["safe"]:
            first_hint = get_safe_fallback()
            leakage    = {"safe": True, "stage": "fallback"}

        return {
            "mode":           "screenshot",
            "success":        True,
            "problem_title":  info.get("problem_title", "Unknown"),
            "difficulty":     info.get("difficulty", "Unknown"),
            "pattern":        info.get("pattern", ""),
            "constraints":    info.get("key_constraints", []),
            "confidence":     info.get("pattern_confidence", "medium"),
            "response":       first_hint,
            "leakage_result": leakage,
            "raw_text":       raw_text[:200],
        }

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
    def analyze_code(
        self,
        code: str,
        problem_title: str = "",
        difficulty: str = "Medium",
        pattern: str = "",
    ) -> dict:
        """Analyze student code and give a targeted Socratic hint about the bottleneck."""
        from prompts.templates import CODE_ANALYSIS_SYSTEM, CODE_ANALYSIS_PROMPT
        from engine.gemini_client import generate_text
        from engine.leakage_gate import check_hint, get_safe_fallback

        self.session.mode_counts["code_analysis"] = (
            self.session.mode_counts.get("code_analysis", 0) + 1
        )

        prompt = CODE_ANALYSIS_PROMPT.format(
            problem_title=problem_title or "Unknown Problem",
            difficulty=difficulty,
            pattern=pattern or "unknown",
            code=code,
        )

        try:
            response = generate_text(prompt, system=CODE_ANALYSIS_SYSTEM)
        except Exception as e:
            response = f"Could not analyze code: {e}"

        leakage = check_hint(response, use_semantic=False)
        if not leakage["safe"]:
            response = get_safe_fallback()
            leakage = {"safe": True, "stage": "fallback"}

        self.session.total_hints += 1
        return {
            "mode":         "code_analysis",
            "response":     response,
            "leakage_result": leakage,
            "problem_title": problem_title,
            "session_hints": self.session.total_hints,
            "leakage_rate": round(self.session.leakage_rate, 4),
        }