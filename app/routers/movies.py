from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import models, schemas
from app.dependencies import get_movie_or_404

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

# 2. Фильмдерді пагинация және фильтрация арқылы алу (Read)
@router.get("/", response_model=List[schemas.MovieResponse])
def get_all_movies(
    skip: int = Query(0, ge=0),          # Өткізіп жіберу саны
    limit: int = Query(10, ge=1, le=100), # Фильмдерге лимит
    genre: Optional[str] = None,         # Жанр бойынша фильтрация
    db: Session = Depends(get_db)
):
    query = db.query(models.Movie)
    
    # Егер жанр берілсе, фильтірді қолдану
    if genre:
        query = query.filter(models.Movie.genre == genre)
    
    # Пагинацияны қолдану
    movies = query.offset(skip).limit(limit).all()
    return movies

# 3. Фильмді жаңарту (Update)
@router.put("/{movie_id}", response_model=schemas.MovieResponse)
def update_movie(
    updated_movie: schemas.MovieCreate, 
    db: Session = Depends(get_db),
    db_movie: models.Movie = Depends(get_movie_or_404) 
):
    db_movie.title = updated_movie.title
    db_movie.description = updated_movie.description
    db_movie.genre = updated_movie.genre
    db_movie.release_year = updated_movie.release_year
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

# 4. Фильмді өшіру (Delete)
@router.delete("/{movie_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    db: Session = Depends(get_db),
    db_movie: models.Movie = Depends(get_movie_or_404)
):
    db.delete(db_movie)
    db.commit()
    return None