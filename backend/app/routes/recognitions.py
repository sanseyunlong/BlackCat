from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.image import Image
from app.models.recognition import Recognition
from app.config import settings
from app.services.ai_provider import classify_image
from app.services.rate_limit import limiter


router = APIRouter(prefix="/recognitions", tags=["recognitions"])


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


@router.post("/{image_id}")
@limiter.limit("30/minute")
async def recognize(request: Request, image_id: int, db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    # 先查缓存
    cached = (
        db.query(Recognition)
        .filter(Recognition.image_id == image.id, Recognition.model == settings.model_name)
        .first()
    )
    if cached:
        return {
            "label_en": cached.label_en,
            "label_zh": cached.label_zh or "",
            "phonetic": cached.phonetic or "",
            "confidence": cached.confidence,
            "model": cached.model
        }
    # 读取文件并调用外部 API
    with open(image.file_path, "rb") as f:
        content = f.read()
    label_en, label_zh, phonetic, conf, raw_resp = await classify_image(content)
    rec = Recognition(
        image_id=image.id,
        label_en=label_en,
        label_zh=label_zh,
        phonetic=phonetic,
        confidence=conf,
        model=settings.model_name,
        raw_response=raw_resp
    )
    db.add(rec)
    db.commit()
    return {
        "label_en": label_en,
        "label_zh": label_zh,
        "phonetic": phonetic,
        "confidence": conf,
        "model": settings.model_name
    }


@router.get("/{image_id}")
def get_recognition(image_id: int, db: Session = Depends(get_db)):
    rec = db.query(Recognition).filter(Recognition.image_id == image_id).first()
    if not rec:
        raise HTTPException(status_code=404, detail="未找到识别结果")
    return {
        "label_en": rec.label_en,
        "label_zh": rec.label_zh or "",
        "phonetic": rec.phonetic or "",
        "confidence": rec.confidence,
        "model": rec.model
    }