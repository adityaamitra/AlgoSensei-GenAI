"""
auth/security.py
────────────────
Password hashing and JWT token management.
"""
import os
import hashlib
import hmac
import base64
import json
import time
from typing import Optional

# Secret key — override with JWT_SECRET in .env for production
SECRET_KEY = os.environ.get("JWT_SECRET", "algosensei-dev-secret-change-in-production")
ALGORITHM  = "HS256"
TOKEN_EXPIRE_DAYS = 30


# ── Password hashing (using stdlib hashlib — no bcrypt needed) ──

def hash_password(password: str) -> str:
    """Hash password using PBKDF2-HMAC-SHA256."""
    salt = os.urandom(32)
    key  = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 200_000)
    return base64.b64encode(salt + key).decode()

def verify_password(password: str, hashed: str) -> bool:
    """Verify password against stored hash."""
    try:
        raw  = base64.b64decode(hashed.encode())
        salt = raw[:32]
        stored_key = raw[32:]
        key  = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 200_000)
        return hmac.compare_digest(key, stored_key)
    except Exception:
        return False


# ── JWT tokens (manual implementation — no python-jose needed) ──

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def _b64url_decode(s: str) -> bytes:
    padding = 4 - len(s) % 4
    return base64.urlsafe_b64decode(s + '=' * padding)

def create_token(user_id: int, email: str, username: str) -> str:
    """Create a JWT token."""
    header  = _b64url_encode(json.dumps({"alg": ALGORITHM, "typ": "JWT"}).encode())
    payload = _b64url_encode(json.dumps({
        "sub":      str(user_id),
        "email":    email,
        "username": username,
        "exp":      int(time.time()) + TOKEN_EXPIRE_DAYS * 86400,
        "iat":      int(time.time()),
    }).encode())
    sig_input = f"{header}.{payload}".encode()
    sig = hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest()
    return f"{header}.{payload}.{_b64url_encode(sig)}"

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT and return payload, or None if invalid/expired."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        header, payload, sig = parts
        sig_input = f"{header}.{payload}".encode()
        expected_sig = hmac.new(SECRET_KEY.encode(), sig_input, hashlib.sha256).digest()
        if not hmac.compare_digest(_b64url_decode(sig), expected_sig):
            return None
        data = json.loads(_b64url_decode(payload))
        if data.get("exp", 0) < time.time():
            return None
        return data
    except Exception:
        return None
