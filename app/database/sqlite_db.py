"""
SQLite database layer.
Used as the primary database (works without any external setup).
MongoDB version can be swapped in via app/database/mongo_db.py.

Tables:
  users      — registered user accounts
  tasks      — tasks owned by users
"""
import sqlite3
from app.config import settings


def get_db() -> sqlite3.Connection:
    """Return a new SQLite connection with dict-like row access."""
    conn = sqlite3.connect(settings.SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    """Create all tables if they don't exist. Called once at startup."""
    conn = get_db()

    # ── Users table ────────────────────────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id              TEXT PRIMARY KEY,           -- UUID string
            username        TEXT NOT NULL UNIQUE,
            email           TEXT NOT NULL UNIQUE,
            hashed_password TEXT NOT NULL,
            created_at      TEXT DEFAULT (datetime('now'))
        )
    """)

    # ── Tasks table ────────────────────────────────────────────────────────────
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id          TEXT PRIMARY KEY,              -- UUID string
            title       TEXT NOT NULL,
            description TEXT,
            status      TEXT NOT NULL DEFAULT 'pending'
                        CHECK(status IN ('pending', 'in_progress', 'completed')),
            user_id     TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            updated_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()
