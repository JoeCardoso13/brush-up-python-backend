"""SQLite-backed per-user token budget tracking."""

import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_INPUT_BUDGET = int(os.environ.get("BRUSH_UP_INPUT_BUDGET", "2000000"))
DEFAULT_OUTPUT_BUDGET = int(os.environ.get("BRUSH_UP_OUTPUT_BUDGET", "500000"))

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    user_id            TEXT PRIMARY KEY,
    total_input_tokens  INTEGER NOT NULL DEFAULT 0,
    total_output_tokens INTEGER NOT NULL DEFAULT 0,
    created_at         TEXT NOT NULL,
    last_active        TEXT NOT NULL
)
"""


def init_db(db_path: Path | str = ":memory:") -> sqlite3.Connection:
    """Open (or create) the budget database and return a connection."""
    conn = sqlite3.connect(str(db_path), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute(_CREATE_TABLE)
    conn.commit()
    return conn


def _ensure_user(conn: sqlite3.Connection, user_id: str) -> None:
    """Insert a user row if it doesn't exist yet."""
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        "INSERT OR IGNORE INTO users (user_id, created_at, last_active) VALUES (?, ?, ?)",
        (user_id, now, now),
    )
    conn.commit()


def check_budget(
    conn: sqlite3.Connection,
    user_id: str,
    max_input_tokens: int = DEFAULT_INPUT_BUDGET,
    max_output_tokens: int = DEFAULT_OUTPUT_BUDGET,
) -> bool:
    """Return True if the user is still within budget."""
    _ensure_user(conn, user_id)
    row = conn.execute(
        "SELECT total_input_tokens, total_output_tokens FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    return (
        row["total_input_tokens"] < max_input_tokens
        and row["total_output_tokens"] < max_output_tokens
    )


def record_usage(
    conn: sqlite3.Connection,
    user_id: str,
    input_tokens: int,
    output_tokens: int,
) -> dict:
    """Add tokens to a user's totals. Returns updated totals."""
    _ensure_user(conn, user_id)
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """UPDATE users
           SET total_input_tokens  = total_input_tokens  + ?,
               total_output_tokens = total_output_tokens + ?,
               last_active = ?
         WHERE user_id = ?""",
        (input_tokens, output_tokens, now, user_id),
    )
    conn.commit()
    return get_usage(conn, user_id)


def get_usage(conn: sqlite3.Connection, user_id: str) -> dict | None:
    """Return current token totals for a user, or None if not found."""
    row = conn.execute(
        "SELECT total_input_tokens, total_output_tokens FROM users WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    if row is None:
        return None
    return {
        "total_input_tokens": row["total_input_tokens"],
        "total_output_tokens": row["total_output_tokens"],
    }
