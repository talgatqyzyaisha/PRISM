from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# --- Фильмдерге арналған схемалар (Movie) ---
class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None

class MovieCreate(MovieBase):
    pass  # Фильм қосқанда осы деректерді талап етеміз

class MovieResponse(MovieBase):
    id: int

    class Config:
        from_attributes = True  # SQLAlchemy модельдерін Pydantic-ке автоматты түрде айналдыру үшін


# --- Пайдаланушыларға арналған схемалар (User) ---
class UserBase(BaseModel):
    email: EmailStr
    role: str = "critic"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

# --- Рецензияларға арналған схемалар (Review) ---
class ReviewBase(BaseModel):
    score: float
    comment: Optional[str] = None
    movie_id: int
    critic_id: int

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(BaseModel):
    id: int
    score: float
    comment: Optional[str] = None
    created_at: datetime
    critic_id: int  # Тек кім жазғанын қалдырамыз, фильмді қайта жүктемейміз (цикл болмас үшін)

    class Config:
        from_attributes = True
        
# Күрделі сұранысқа арналған арнайы схема (Фильм + оның рецензиялары)
class MovieDetailResponse(MovieResponse):
    reviews: List[ReviewResponse] = []  # Рецензиялар тізімін осы жерде қайтарамыз

# --- Шешімдер журналына арналған схемалар (DecisionLog) ---
class DecisionCreate(BaseModel):
    verdict: str  # "APPROVED" немесе "REJECTED"
    reason: Optional[str] = None
    movie_id: int

class DecisionResponse(BaseModel):
    id: int
    verdict: str
    reason: Optional[str] = None
    created_at: datetime
    movie_id: int
    director_id: int

    class Config:
        from_attributes = True