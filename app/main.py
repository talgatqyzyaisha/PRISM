from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import engine, Base, SessionLocal, get_db
from app.routers import movies, users, reviews, decisions
from app.utils import hash_password

# Жүйе іске қосылғанда ДҚ кестелерді автоматты түрде құру
Base.metadata.create_all(bind=engine)

def init_db():
    print("ДБ инициализациясы аяқталды")
    db = SessionLocal()
    try:
        # Егер базада директор, кинокритик, аударманы болмаса, автоматты түрде қосамыз
        users_data = {
            "director@prism.kz": {"role": "director", "password": "director123"},
            "critic@prism.kz": {"role": "critic", "password": "critic123"},
            "translator@prism.kz": {"role": "translator", "password": "translator123"}
        }
        for email, info in users_data.items():
            if not db.query(models.User).filter(models.User.email == email).first():
                user = models.User(email=email, hashed_password=hash_password(info["password"]), role=info["role"])
                db.add(user)
        
        # Егер базада фильм болмаса, сынақ фильм қосамыз
        if not db.query(models.Movie).filter(models.Movie.title == "Тест Фильм").first():
            movie = models.Movie(title="Тест Фильм", description="Сынақ сипаттамасы", genre="Драма", release_year=2024)
            db.add(movie)
        
        db.commit()
    except Exception as e:
        print(f"Инициализация кезінде қате: {e}")
        db.rollback()
    finally:
        db.close()
init_db()

app = FastAPI(
    title="Prism API",
    description="Медиаконтентті бағалау және тәуекелдерді талдау жүйесі",
    version="1.0.0"
)

# CORS баптаулары (болашақта фронтенд сұраныстар жібере алуы үшін)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Роутерлерді жүйеге қосу
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(reviews.router)
app.include_router(decisions.router)

# Күрделі сұраныс: Фильмді барлық рецензияларымен бірге алу (JOIN)
@app.get("/movies/{movie_id}/details", response_model=schemas.MovieDetailResponse, tags=["Advanced Queries (Күрделі сұраныстар)"])
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Фильм табылмады!")

    reviews_count = db.query(models.Review).filter(models.Review.movie_id == movie_id).count()
    
    return {
        "id": movie.id,
        "title": movie.title,
        "genre": movie.genre,
        "release_year": movie.release_year,
        "reviews_count": reviews_count,
        "reviews": movie.reviews  
    }
    
@app.get("/")
def read_root():
    return {"message": "Prism API-ге қош келдіңіз! Жүйе сәтті жұмыс істеп тұр."}