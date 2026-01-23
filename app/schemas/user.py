from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Schema for user registration/login."""
    username: str
    password: str = Field(..., min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str