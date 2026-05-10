"""
Internal data models for User.
These represent how data is stored in the database,
not how it's exposed in the API (see schemas/).
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    id: str
    username: str
    email: str
    hashed_password: str
    created_at: Optional[str] = None
