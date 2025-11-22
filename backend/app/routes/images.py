import hashlib
import os
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.image import Image
from app.models.user import User
from app.config import settings
from app.services.rate_limit import limiter


router = APIRouter(prefix="/images", tags=["images"])


@router.get("/debug-auth")
async def debug_auth(request: Request):
    """调试用：检查认证状态"""
    token = request.cookies.get("access_token")
    csrf = request.cookies.get("csrf_token")
    user_id = _get_user_id(request)
    return {
        "has_access_token": bool(token),
        "access_token_preview": token[:20] + "..." if token else None,
        "has_csrf_token": bool(csrf),
        "user_id": user_id,
        "cookies": dict(request.cookies)
    }


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _get_user_id(request: Request) -> Optional[int]:
    token = request.cookies.get("access_token")
    if not token:
        return None
    from jose import jwt, JWTError
    try:
        data = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        return int(data.get("sub"))
    except JWTError:
        return None


@router.post("")
@limiter.limit("20/minute")
async def upload_image(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    user_id = _get_user_id(request)
    if not user_id:
        raise HTTPException(status_code=401, detail="未登录")
    # 读取文件并计算哈希
    content = await file.read()
    if len(content) > 10 * 1024 * 1024:  # 10MB 限制
        raise HTTPException(status_code=413, detail="图片过大，最大支持10MB")
    image_hash = hashlib.sha256(content).hexdigest()
    # 保存文件
    upload_dir = os.path.join("backend", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{image_hash}.jpg")
    with open(file_path, "wb") as f:
        f.write(content)
    img = Image(user_id=user_id, image_hash=image_hash, file_path=file_path)
    db.add(img)
    db.commit()
    db.refresh(img)
    return {"image_id": img.id, "image_hash": image_hash}


@router.get("/{image_id}")
async def get_image(image_id: int, db: Session = Depends(get_db)):
    """获取图片文件"""
    image = db.query(Image).filter(Image.id == image_id).first()
    if not image:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    if not os.path.exists(image.file_path):
        raise HTTPException(status_code=404, detail="图片文件不存在")
    
    return FileResponse(image.file_path, media_type="image/jpeg")