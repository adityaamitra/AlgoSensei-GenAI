"""
auth/routes.py
────────────────
FastAPI routes for auth + progress.
"""
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional
import sqlite3

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ── Models ──────────────────────────────────────────────────

class SignupReq(BaseModel):
    email: str
    username: str
    password: str

class LoginReq(BaseModel):
    email: str
    password: str

class ProgressReq(BaseModel):
    problem_id: int
    problem_title: str
    pattern: str = ""
    difficulty: str = "Medium"
    status: str = "solved"
    hints_used: int = 0

class FeedbackReq(BaseModel):
    problem_id: Optional[int] = None
    problem_title: str = ""
    hint_level: Optional[int] = None
    hint_text: str = ""
    was_helpful: int = 1


# ── Auth helpers ─────────────────────────────────────────────

def get_current_user(request: Request) -> Optional[dict]:
    """Extract user from Authorization header."""
    from auth.security import verify_token
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    return verify_token(auth[7:])

def require_user(request: Request) -> dict:
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


# ── Routes ───────────────────────────────────────────────────

@router.post("/signup")
def signup(req: SignupReq):
    from auth.database import get_db
    from auth.security import hash_password, create_token

    if len(req.password) < 6:
        raise HTTPException(400, "Password must be at least 6 characters")
    if len(req.username) < 3:
        raise HTTPException(400, "Username must be at least 3 characters")
    if "@" not in req.email:
        raise HTTPException(400, "Invalid email address")

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (email, username, hashed_pw) VALUES (?, ?, ?)",
            (req.email.lower(), req.username, hash_password(req.password))
        )
        db.commit()
        row = db.execute("SELECT id FROM users WHERE email=?", (req.email.lower(),)).fetchone()
        token = create_token(row["id"], req.email.lower(), req.username)
        return {"token": token, "username": req.username, "email": req.email.lower()}
    except sqlite3.IntegrityError as e:
        if "email" in str(e):
            raise HTTPException(400, "Email already registered")
        raise HTTPException(400, "Username already taken")
    finally:
        db.close()

@router.post("/login")
def login(req: LoginReq):
    from auth.database import get_db
    from auth.security import verify_password, create_token

    db = get_db()
    try:
        row = db.execute(
            "SELECT * FROM users WHERE email=?", (req.email.lower(),)
        ).fetchone()
        if not row or not verify_password(req.password, row["hashed_pw"]):
            raise HTTPException(401, "Invalid email or password")
        db.execute(
            "UPDATE users SET last_login=datetime('now') WHERE id=?", (row["id"],)
        )
        db.commit()
        token = create_token(row["id"], row["email"], row["username"])
        return {"token": token, "username": row["username"], "email": row["email"]}
    finally:
        db.close()

@router.get("/me")
def me(request: Request):
    user = require_user(request)
    db = get_db() if False else __import__('auth.database', fromlist=['get_db']).get_db()
    try:
        row = db.execute("SELECT id,email,username,created_at,last_login FROM users WHERE id=?",
                         (int(user["sub"]),)).fetchone()
        if not row:
            raise HTTPException(404, "User not found")
        return dict(row)
    finally:
        db.close()

@router.post("/progress")
def save_progress(req: ProgressReq, request: Request):
    from auth.database import get_db
    user = require_user(request)
    db = get_db()
    try:
        db.execute("""
            INSERT INTO progress (user_id, problem_id, problem_title, pattern, difficulty, status, hints_used, solved_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CASE WHEN ? = 'solved' THEN datetime('now') ELSE NULL END, datetime('now'))
            ON CONFLICT(user_id, problem_id) DO UPDATE SET
                status     = excluded.status,
                hints_used = MAX(hints_used, excluded.hints_used),
                solved_at  = CASE WHEN excluded.status = 'solved' AND solved_at IS NULL THEN datetime('now') ELSE solved_at END,
                updated_at = datetime('now')
        """, (int(user["sub"]), req.problem_id, req.problem_title,
              req.pattern, req.difficulty, req.status, req.hints_used, req.status))
        db.commit()
        return {"saved": True}
    finally:
        db.close()

@router.get("/progress")
def get_progress(request: Request):
    from auth.database import get_db
    user = require_user(request)
    db = get_db()
    try:
        rows = db.execute(
            "SELECT * FROM progress WHERE user_id=? ORDER BY updated_at DESC",
            (int(user["sub"]),)
        ).fetchall()
        solved  = [dict(r) for r in rows if r["status"] == "solved"]
        attempted = [dict(r) for r in rows if r["status"] == "attempted"]
        return {
            "solved":    solved,
            "attempted": attempted,
            "total_solved": len(solved),
            "total_attempted": len(attempted),
        }
    finally:
        db.close()

@router.post("/feedback")
def save_feedback(req: FeedbackReq, request: Request):
    from auth.database import get_db
    user = require_user(request)
    db = get_db()
    try:
        db.execute("""
            INSERT INTO hint_history (user_id, problem_id, problem_title, hint_level, hint_text, was_helpful)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (int(user["sub"]), req.problem_id, req.problem_title,
              req.hint_level, req.hint_text[:500], req.was_helpful))
        db.commit()
        return {"saved": True}
    finally:
        db.close()

@router.delete("/account")
def delete_account(request: Request):
    from auth.database import get_db
    user = require_user(request)
    db = get_db()
    try:
        uid = int(user["sub"])
        db.execute("DELETE FROM hint_history WHERE user_id=?", (uid,))
        db.execute("DELETE FROM progress WHERE user_id=?", (uid,))
        db.execute("DELETE FROM users WHERE id=?", (uid,))
        db.commit()
        return {"deleted": True}
    finally:
        db.close()
