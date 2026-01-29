from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.expense import TransactionDB, TransactionType as ModelTransactionType
from app.models.user import UserDB

from app.schemas.expense import CreateTransaction, UpdateTransaction, TransactionResponse, BalanceResponse
from app.core.limiter import limiter

router = APIRouter(
    prefix="/api",
    tags=["transactions"], 
)

def create_transaction_internal(data: CreateTransaction, type_val: Optional[ModelTransactionType], username: str, db: Session):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if type_val is None:
        type_str = data.type.value if hasattr(data.type, "value") else data.type
        type_enum = ModelTransactionType(type_str)
    else:
        type_enum = type_val
        
    transaction = TransactionDB(
        amount=data.amount,
        category=data.category,
        description=data.description,
        type=type_enum,
        owner_id=user.id
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.post("/create_expense", response_model=TransactionResponse)
@limiter.limit("5/minute")
def create_expense(
    request: Request,
    data: CreateTransaction,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_transaction_internal(data, ModelTransactionType.EXPENSE, username, db)


@router.post("/create_income", response_model=TransactionResponse)
@limiter.limit("5/minute")
def create_income(
    request: Request,
    data: CreateTransaction, 
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_transaction_internal(data, ModelTransactionType.INCOME, username, db)


@router.get("/get_balance", response_model=BalanceResponse)
@limiter.limit("10/minute")
def get_balance(
    request: Request,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    results = db.query(
        func.sum(case((TransactionDB.type == ModelTransactionType.INCOME, TransactionDB.amount), else_=0)),
        func.sum(case((TransactionDB.type == ModelTransactionType.EXPENSE, TransactionDB.amount), else_=0))
    ).filter(TransactionDB.owner_id == user.id).first()

    total_income = results[0] or 0
    total_expense = results[1] or 0
    
    current_balance = total_income - total_expense

    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "current_balance": current_balance
    }


@router.get("/get", response_model=List[TransactionResponse])
@limiter.limit("10/minute")
def get_transactions(
    request: Request,
    limit: int = Query(10, ge=1, le=100, description="Number of records"),
    offset: int = Query(0, ge=0, description="Offset"),
    category: Optional[str] = Query(None, description="Filter by category"),
    type: Optional[ModelTransactionType] = Query(None, description="Filter by type (income/expense)"), 
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    min_amount: Optional[int] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[int] = Query(None, ge=0, description="Maximum amount"),
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        return []

    query = db.query(TransactionDB).filter(TransactionDB.owner_id == user.id)

    if category:
        query = query.filter(TransactionDB.category == category)
    if type: 
        query = query.filter(TransactionDB.type == type)
    if start_date:
        query = query.filter(TransactionDB.created_at >= start_date)
    if end_date:
        query = query.filter(TransactionDB.created_at <= end_date)
    if min_amount is not None:
        query = query.filter(TransactionDB.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(TransactionDB.amount <= max_amount)

    return query.order_by(TransactionDB.created_at.desc()).offset(offset).limit(limit).all()


@router.delete("/delete/{transaction_id}")
@limiter.limit("10/minute")
def delete_transaction(
    request: Request,
    transaction_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = (
        db.query(TransactionDB)
        .filter(
            TransactionDB.id == transaction_id,
            TransactionDB.owner_id == user.id,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found or access denied")

    db.delete(transaction)
    db.commit()

    return {"message": "Transaction deleted"}


@router.put("/update/{transaction_id}", response_model=TransactionResponse)
@limiter.limit("10/minute")
def update_transaction(
    request: Request,
    transaction_id: int,
    data: UpdateTransaction,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    transaction = (
        db.query(TransactionDB)
        .filter(
            TransactionDB.id == transaction_id,
            TransactionDB.owner_id == user.id,
        )
        .first()
    )

    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found or access denied")

    if data.amount is not None:
        transaction.amount = data.amount
    if data.category is not None:
        transaction.category = data.category
    if data.description is not None:
        transaction.description = data.description

    db.commit()
    db.refresh(transaction)

    return transaction