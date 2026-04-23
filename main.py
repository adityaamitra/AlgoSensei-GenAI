"""
main.py — AlgoSensei FastAPI Backend
Serves the HTML frontend + API endpoints.
Run: uvicorn main:app --host 0.0.0.0 --port 7860
"""
import sys, os, json, base64
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="AlgoSensei API")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ── Lazy engine singleton ────────────────────────────────────
_engine = None
def get_engine():
    global _engine
    if _engine is None:
        from engine.tutor import AlgoSenseiEngine
        _engine = AlgoSenseiEngine()
    return _engine


# ── Models ───────────────────────────────────────────────────
class HintReq(BaseModel):
    problem: str
    difficulty: str = "Medium"
    pattern: str = ""
    student_context: str = ""
    hint_level: Optional[int] = None

class ExplainReq(BaseModel):
    topic: str
    pattern: str = ""


# ── API routes ───────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/hint")
def hint(req: HintReq):
    try:
        eng = get_engine()
        result = eng.hint(
            problem_title=req.problem,
            difficulty=req.difficulty,
            pattern=req.pattern,
            student_context=req.student_context,
            hint_level=req.hint_level,
        )
        return {
            "response":     result.get("response",""),
            "hint_level":   result.get("hint_level"),
            "safe":         result.get("leakage_result",{}).get("safe", True),
            "sources":      [{"label": c["source"], "score": c["score"],
                              "text": c["text"][:200]}
                             for c in result.get("retrieved_chunks", [])],
            "leakage_rate": result.get("leakage_rate", 0),
            "total_hints":  result.get("session_hints", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/explain")
def explain(req: ExplainReq):
    try:
        eng = get_engine()
        result = eng.explain(req.topic, pattern=req.pattern)
        return {
            "response":    result.get("response",""),
            "sources":     [{"label": c["source"], "score": c["score"],
                             "text": c["text"][:200]}
                            for c in result.get("retrieved_chunks",[])],
            "faithfulness": result.get("faithfulness",{}).get("coverage",0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/screenshot")
async def screenshot(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        eng = get_engine()
        result = eng.analyze_screenshot(image_bytes)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
def stats():
    try:
        eng = get_engine()
        return eng.get_session_stats()
    except Exception:
        return {"total_hints":0,"leakage_rate":0.0,"current_problem":"","hint_level":0}

@app.post("/api/reset")
def reset():
    global _engine
    _engine = None
    return {"status": "reset"}

# ── Static files & pages ─────────────────────────────────────
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

@app.get("/")
def root(): return FileResponse(str(static_dir / "index.html"))

@app.get("/tutor")
def tutor(): return FileResponse(str(static_dir / "tutor.html"))

@app.get("/about")
def about(): return FileResponse(str(static_dir / "index.html"))
