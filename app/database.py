import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Егер .env файлында DATABASE_URL көрсетілмесе, автоматты түрде жергілікті SQLite іске қосылады
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prism.db")

# SQLite үшін арнайы баптау қажет, ал PostgreSQL үшін қажет емес
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ДҚ сессиясын алуға арналған функция (эндпоинттерде қолданылады)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()