"""
Pydantic schemas for task management endpoints.
Defines request validation and response serialisation for all task routes.
"""
from pydantic import BaseModel, Field
from typing import Optional, Literal


class CreateTaskRequest(BaseModel):
    """Request body for POST /tasks"""
    title: str = Field(..., min_length=1, max_length=200,
                       description="Task title")
    description: Optional[str] = Field(None, max_length=1000,
                                       description="Optional task description")
    status: Literal["pending", "in_progress", "completed"] = "pending"


class UpdateTaskRequest(BaseModel):
    """Request body for PUT /tasks/{id} — all fields optional"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[Literal["pending", "in_progress", "completed"]] = None


class TaskResponse(BaseModel):
    """Response body for task endpoints"""
    id: str
    title: str
    description: Optional[str] = None
    status: str
    user_id: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class TaskListResponse(BaseModel):
    """Response body for GET /tasks"""
    total: int
    tasks: list[TaskResponse]
