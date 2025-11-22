from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.image import Image
from app.models.recognition import Recognition
from app.config import settings


router = APIRouter(prefix="/records", tags=["records"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_user_id(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return None
    from jose import jwt, JWTError
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return int(data.get("sub"))
    except JWTError:
        return None


@router.get("")
def list_records(request: Request, date: Optional[str] = None, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not user_id:
        return {"items": []}
    q = db.query(Recognition).join(Image, Recognition.image_id == Image.id).filter(Image.user_id == user_id)
    if date:
        # 简单过滤同日记录（按 UTC 日期前缀）
        try:
            d = datetime.strptime(date, "%Y-%m-%d").date()
            next_d = datetime.strptime(date, "%Y-%m-%d").date()
        except Exception:
            d = None
        if d:
            # 由于 SQLite 日期函数支持有限，直接取所有记录在前端筛选更稳妥
            pass
    items = [
        {
            "id": r.id,
            "label_en": r.label_en,
            "label_zh": r.label_zh or "",
            "phonetic": r.phonetic or "",
            "confidence": r.confidence,
            "image_id": r.image_id,
            "created_at": str(r.created_at),
        }
        for r in q.order_by(Recognition.id.desc()).all()
    ]
    return {"items": items}


@router.delete("/{record_id}")
def delete_record(request: Request, record_id: int, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")
    
    # 查找记录并验证所有权
    record = db.query(Recognition).filter(Recognition.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    
    # 验证记录属于当前用户
    image = db.query(Image).filter(Image.id == record.image_id).first()
    if not image or image.user_id != user_id:
        raise HTTPException(status_code=403, detail="无权删除此记录")
    
    # 删除记录
    db.delete(record)
    db.commit()
    
    return {"message": "删除成功"}