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