from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews (Рецензиялар)"]
)

# 1. Жаңа рецензия қосу (Баға қою)
@router.post("/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    # Валидация: баға 0 мен 10 аралығында болуы тиіс
    if review.score < 0 or review.score > 10:
        raise HTTPException(status_code=400, detail="Баға 0 мен 10 аралығында болуы керек!")

    # Фильмнің базада бар-жоғын тексеру
    movie = db.query(models.Movie).filter(models.Movie.id == review.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Мұндай фильм табылмады!")

    # Критиктің базада бар-жоғын тексеру
    critic = db.query(models.User).filter(models.User.id == review.critic_id).first()
    if not critic:
        raise HTTPException(status_code=404, detail="Мұндай пайдаланушы табылмады!")

    # Жаңа рецензияны сақтау
    db_review = models.Review(
        score=review.score,
        comment=review.comment,
        movie_id=review.movie_id,
        critic_id=review.critic_id
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

# 2. Белгілі бір фильмнің барлық рецензияларын алу
@router.get("/movie/{movie_id}", response_model=List[schemas.ReviewResponse])
def get_movie_reviews(movie_id: int, db: Session = Depends(get_db)):
    return db.query(models.Review).filter(models.Review.movie_id == movie_id).all()