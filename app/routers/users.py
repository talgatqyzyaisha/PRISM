from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, utils

router = APIRouter(
    prefix="/users",
    tags=["Users (Пайдаланушылар)"]
)

# 1. Жаңа пайдаланушыны тіркеу (Регистрация)
@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Email-дің бірегейлігін тексеру
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Бұл email жүйеде тіркелген!"
        )
    
    # Парольді хэштеп, жаңа пайдаланушыны құру
    hashed_pwd = utils.hash_password(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. Барлық пайдаланушылар тізімін алу
@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()