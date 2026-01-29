from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class CreateTransaction(BaseModel):
    """Schema for creating a transaction."""
    amount: int = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=100)
    type: TransactionType = TransactionType.EXPENSE


class UpdateTransaction(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[int] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=40)
    description: Optional[str] = Field(None, max_length=100)
    type: Optional[TransactionType] = None

class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    amount: int
    category: str
    description: Optional[str]
    created_at: datetime
    type: TransactionType

    class Config:
        from_attributes = True


class BalanceResponse(BaseModel):
    """Schema for balance response."""
    total_income: int
    total_expense: int
    current_balance: int