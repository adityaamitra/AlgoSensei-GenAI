"""
auth/database.py
────────────────
SQLite database for users and progress.
Zero external dependencies — just Python's built-in sqlite3.
"""
import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "algosensei.db"

def get_db():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Create all tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email       TEXT    UNIQUE NOT NULL,
            username    TEXT    UNIQUE NOT NULL,
            hashed_pw   TEXT    NOT NULL,
            created_at  TEXT    DEFAULT (datetime('now')),
            last_login  TEXT
        );

        CREATE TABLE IF NOT EXISTS progress (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            problem_id  INTEGER NOT NULL,
            problem_title TEXT  NOT NULL,
            pattern     TEXT,
            difficulty  TEXT,
            status      TEXT    DEFAULT 'attempted',
            hints_used  INTEGER DEFAULT 0,
            solved_at   TEXT,
            updated_at  TEXT    DEFAULT (datetime('now')),
            UNIQUE(user_id, problem_id)
        );

        CREATE TABLE IF NOT EXISTS hint_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            problem_id  INTEGER,
            problem_title TEXT,
            hint_level  INTEGER,
            hint_text   TEXT,
            was_helpful INTEGER,
            created_at  TEXT    DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_progress_user ON progress(user_id);
        CREATE INDEX IF NOT EXISTS idx_hints_user ON hint_history(user_id);
    """)
    conn.commit()
    conn.close()
