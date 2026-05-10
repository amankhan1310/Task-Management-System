"""
Pydantic schemas for authentication endpoints.
These define what the API accepts (request) and returns (response).
Separate from internal models — keeps API contract and DB structure decoupled.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional


class RegisterRequest(BaseModel):
    """Request body for POST /register"""
    username: str = Field(..., min_length=3, max_length=50,
                          description="Unique username (3–50 chars)")
    email: EmailStr
    password: str = Field(..., min_length=8,
                          description="Password — minimum 8 characters")

    @field_validator("username")
    @classmethod
    def username_must_be_alphanumeric(cls, v: str) -> str:
        """Only letters, digits, and underscores allowed in username."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Username may only contain letters, digits, and underscores.")
        return v.lower()


class LoginRequest(BaseModel):
    """Request body for POST /login"""
    username: str
    password: str


class TokenResponse(BaseModel):
    """Response body for POST /login"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Token TTL in seconds")


class UserResponse(BaseModel):
    """Safe user profile — never includes hashed_password"""
    id: str
    username: str
    email: str
    created_at: Optional[str] = None
