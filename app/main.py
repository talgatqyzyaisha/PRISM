from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import movies, users

# Жүйе іске қосылғанда ДҚ кестелерді автоматты түрде құру
Base.metadata.create_all(bind=engine)

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

# Роутерді жүйеге қосу
app.include_router(movies.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Prism API-ге қош келдіңіз! Жүйе сәтті жұмыс істеп тұр."}