from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.db.database import get_db
from app.models.user import UserDB
from app.schemas.user import UserCreate, Token

router = APIRouter(
    prefix="/api",
    tags=["auth"],
)


@router.post("/register")
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    if db.query(UserDB).filter(UserDB.username == data.username).first():
        raise HTTPException(status_code=400, detail="User already exists")

    user = UserDB(
        username=data.username,
        hashed_password=get_password_hash(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully", "user_id": user.id}


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(UserDB)
        .filter(UserDB.username == form_data.username)
        .first()
    )

    if not user or not verify_password(
        form_data.password,
        user.hashed_password,
    ):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    
    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
