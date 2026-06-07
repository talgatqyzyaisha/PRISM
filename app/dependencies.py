from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

def get_movie_or_404(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм табылмады!")
    return movie