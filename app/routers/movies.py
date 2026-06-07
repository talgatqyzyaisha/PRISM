from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/movies",
    tags=["Movies (Фильмдер)"]
)

# 1. Жаңа фильм қосу (Create)
@router.post("/", response_model=schemas.MovieResponse, status_code=status.HTTP_201_CREATED)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    db_movie = models.Movie(
        title=movie.title,
        description=movie.description,
        genre=movie.genre,
        release_year=movie.release_year
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)  # Дерекқордан жаңа ID-ді алу
    return db_movie

# 2. Барлық фильмдер тізімін алу (Read)
@router.get("/", response_model=List[schemas.MovieResponse])
def get_all_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies