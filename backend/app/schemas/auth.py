from pydantic import BaseModel, EmailStr
from typing import Optional


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for decoded token data."""
    id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None  # "user" or "teacher"


class LoginRequest(BaseModel):
    """Schema for login request."""
    email: EmailStr
    password: str
