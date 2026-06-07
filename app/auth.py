from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app import models
from app.database import get_db
from sqlalchemy.orm import Session

# Swagger-де "Authorize" батырмасын іске қосу үшін қолданылады
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Бұл функция токенді тексереді және ағымдағы пайдаланушыны (user) қайтарады.
    """
    # 1. Токеннің бар-жоғын тексеру
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Токен қажет!"
        )
    
    try:
        # 2. Жүйені жеңілдету үшін токенді пайдаланушының ID-і деп есептейміз
        user_id = int(token) 
        
        # 3. Дерекқордан пайдаланушыны іздеу
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        # 4. Егер пайдаланушы табылмаса, қате жіберу
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Пайдаланушы табылмады немесе токен жарамсыз!"
            )
        
        return user # Авторизацияланған пайдаланушыны қайтарамыз
    
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Жарамсыз токен пішімі!"
        )