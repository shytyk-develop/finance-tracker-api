from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateExpense(BaseModel):
    """Schema for creating an expense."""
    amount: int = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=100)


class UpdateExpense(BaseModel):
    """Schema for updating an expense."""
    amount: Optional[int] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=100)


class ExpenseResponse(BaseModel):
    """Schema for expense response."""
    id: int
    amount: int
    category: str
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
