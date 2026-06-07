from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.auth import get_current_user
from app import models, schemas
from app.dependencies import get_movie_or_404

router = APIRouter(
    prefix="/decisions",
    tags=["Decisions (Директор шешімдері)"]
)

# 1. Жаңа шешімді тіркеу (Фильмді қабылдау немесе бас тарту)
@router.post("/", response_model=schemas.DecisionResponse, status_code=status.HTTP_201_CREATED)
def create_decision(decision: schemas.DecisionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user), movie: models.Movie = Depends(get_movie_or_404)):
    # 1. Рөлді тексеру
    if current_user.role != "director":
        raise HTTPException(status_code=403, detail="Бұл әрекетті тек Директор (admin) орындай алады!")
    
    # 2. Вердикт форматын тексеру
    if decision.verdict not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Вердикт тек 'APPROVED' немесе 'REJECTED' болуы тиіс!")

    # 3. Тәуекелдерді талдау
    # Фильмнің критиктерден алған орташа бағасын есептейміз
    reviews = movie.reviews
    final_reason = decision.reason or ""
    
    if reviews:
        avg_score = sum([r.score for r in reviews]) / len(reviews)
        # Егер орташа баға 5-тен төмен болса, бірақ директор мақұлдаса — жүйе автоматты түрде ескерту жазады
        if avg_score < 5.0 and decision.verdict == "APPROVED":
            warning_text = f"[ЖҮЙЕ ЕСКЕРТУІ: Фильмнің критиктер арасындағы рейтингі төмен ({avg_score:.1f}/10)!] "
            final_reason = warning_text + final_reason

    # 4. Шешімді базаға сақтау
    db_decision = models.DecisionLog(
        verdict=decision.verdict,
        reason=final_reason,
        movie_id=decision.movie_id,
        director_id=current_user.id
    )
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision

# 2. Белгілі бір фильмге қатысты қабылданған барлық шешімдерді көру
@router.get("/movie/{movie_id}", response_model=List[schemas.DecisionResponse])
def get_movie_decisions(movie_id: int, skip: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    decisions = db.query(models.DecisionLog)\
        .filter(models.DecisionLog.movie_id == movie_id)\
        .offset(skip)\
        .limit(limit)\
        .all()
    return decisions