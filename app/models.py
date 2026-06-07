from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="critic")  # admin (директор), critic (критик), translator (аудармашы)

    # Байланыстар: бір пайдаланушы көптеген рецензиялар мен шешімдер қалдыра алады
    reviews = relationship("Review", back_populates="author")
    decisions = relationship("DecisionLog", back_populates="director")


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    genre = Column(String, index=True)
    release_year = Column(Integer)

    # Байланыстар: бір фильмнің көптеген рецензиялары мен шешімдер журналы болуы мүмкін
    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")
    decisions = relationship("DecisionLog", back_populates="movie", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)  # Бағалау (1-10 балл)
    comment = Column(Text, nullable=True)   # Критиктің құпия есебі
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    critic_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Кері байланыстар
    movie = relationship("Movie", back_populates="reviews")
    author = relationship("User", back_populates="reviews")


class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(Integer, primary_key=True, index=True)
    verdict = Column(String, nullable=False)  # "APPROVED" (сатып алу) немесе "REJECTED" (бас тарту)
    reason = Column(Text, nullable=True)     # Директордың қабылдаған шешімінің негіздемесі
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    director_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Кері байланыстар
    movie = relationship("Movie", back_populates="decisions")
    director = relationship("User", back_populates="decisions")