"""
Internal data model for Task.
Represents the database structure for a task record.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: str
    title: str
    description: Optional[str]
    status: str          # pending | in_progress | completed
    user_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
