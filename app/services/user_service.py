import uuid
from typing import Optional
from app.database import get_db
from app.auth.security import hash_password, verify_password

def get_user_by_username(username: str) -> Optional[dict]:
    """Return user dict by username, or None if not found."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_email(email: str) -> Optional[dict]:
    """Return user dict by email, or None if not found."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id: str) -> Optional[dict]:
    """Return user dict by ID, or None if not found."""
    conn = get_db()
    row = conn.execute(
        "SELECT * FROM users WHERE id = ?", (user_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def create_user(username: str, email: str, password: str) -> dict:
    """
    Create a new user with hashed password.
    Raises ValueError if username or email already exists.
    """
    if get_user_by_username(username):
        raise ValueError(f"Username '{username}' is already taken.")
    if get_user_by_email(email):
        raise ValueError(f"Email '{email}' is already registered.")

    user_id = str(uuid.uuid4())
    hashed = hash_password(password)

    conn = get_db()
    conn.execute(
        "INSERT INTO users (id, username, email, hashed_password) VALUES (?, ?, ?, ?)",
        (user_id, username, email, hashed)
    )
    conn.commit()
    conn.close()

    return {"id": user_id, "username": username, "email": email}

def authenticate_user(username: str, password: str) -> Optional[dict]:
    """Verify credentials and return the user if valid."""
    user = get_user_by_username(username)
    if not user:
        return None
    
    # Ensure the field name matches your SQLite schema (hashed_password)
    if not verify_password(password, user["hashed_password"]):
        return None
    return user