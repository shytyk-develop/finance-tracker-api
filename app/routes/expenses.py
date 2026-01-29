from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_db
from app.models.expense import ExpenseDB
from app.models.user import UserDB
from app.schemas.expense import CreateExpense, UpdateExpense, ExpenseResponse
from app.core.limiter import limiter

router = APIRouter(
    prefix="/api",
    tags=["expenses"],
)


@router.post("/create", response_model=ExpenseResponse)
@limiter.limit("10/minute")
def create_expense(
    request: Request,
    data: CreateExpense,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = (
        db.query(UserDB)
        .filter(UserDB.username == username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expense = ExpenseDB(
        amount=data.amount,
        category=data.category,
        description=data.description,
        owner_id=user.id,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("/get", response_model=List[ExpenseResponse])
@limiter.limit("10/minute")
def get_expenses(
    request: Request,
    limit: int = Query(10, ge=1, le=100, description="Number of records"),
    offset: int = Query(0, ge=0, description="Offset"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[datetime] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[datetime] = Query(None, description="End date (YYYY-MM-DD)"),
    min_amount: Optional[int] = Query(None, ge=0, description="Minimum amount"),
    max_amount: Optional[int] = Query(None, ge=0, description="Maximum amount"),
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    
    user = (
        db.query(UserDB)
        .filter(UserDB.username == username)
        .first()
    )

    if not user:
        return []

    query = db.query(ExpenseDB).filter(ExpenseDB.owner_id == user.id)

    if category:
        query = query.filter(ExpenseDB.category == category)
    if start_date:
        query = query.filter(ExpenseDB.created_at >= start_date)
    if end_date:
        query = query.filter(ExpenseDB.created_at <= end_date)
    if min_amount is not None:
        query = query.filter(ExpenseDB.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(ExpenseDB.amount <= max_amount)

    return query.order_by(ExpenseDB.created_at.desc()).offset(offset).limit(limit).all()


@router.delete("/delete/{expense_id}")
@limiter.limit("10/minute")
def delete_expense(
    request: Request,
    expense_id: int,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = (
        db.query(UserDB)
        .filter(UserDB.username == username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expense = (
        db.query(ExpenseDB)
        .filter(
            ExpenseDB.id == expense_id,
            ExpenseDB.owner_id == user.id,
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found or access denied",
        )

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}


@router.put("/update/{expense_id}", response_model=ExpenseResponse)
@limiter.limit("10/minute")
def update_expense(
    request: Request,
    expense_id: int,
    data: UpdateExpense,
    username: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = (
        db.query(UserDB)
        .filter(UserDB.username == username)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expense = (
        db.query(ExpenseDB)
        .filter(
            ExpenseDB.id == expense_id,
            ExpenseDB.owner_id == user.id,
        )
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found or access denied",
        )

    if data.amount is not None:
        expense.amount = data.amount
    if data.category is not None:
        expense.category = data.category
    if data.description is not None:
        expense.description = data.description

    db.commit()
    db.refresh(expense)

    return expense
