import enum
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Enum

from app.db.database import Base

class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"

class TransactionDB(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    category = Column(String)
    description = Column(String, nullable=True)
    type = Column(Enum(TransactionType), default=TransactionType.EXPENSE)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
