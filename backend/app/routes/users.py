from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.config import settings


router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/me")
def me(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="未登录")
    from jose import jwt, JWTError
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        user_id = int(data.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="会话无效")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"id": user.id, "email": user.email, "is_verified": user.is_verified}