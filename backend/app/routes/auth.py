from datetime import datetime, timedelta, timezone
import hashlib

from fastapi import APIRouter, Depends, HTTPException, Response, Request
from fastapi import status
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.config import settings
from app.models.user import User
from app.models.email_code import EmailCode
from app.schemas.auth import (
    RegisterRequest,
    VerifyEmailRequest,
    LoginRequest,
    PasswordResetRequest,
    VerifyResetCodeRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.services.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_csrf_token,
    generate_email_code,
)
from app.services.email import send_email
from app.services.rate_limit import limiter


router = APIRouter(prefix="/auth", tags=["auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def _hash_code(code: str) -> str:
    return hashlib.sha256(code.encode()).hexdigest()


@router.post("/register")
@limiter.limit("5/minute")
def register(request: Request, payload: RegisterRequest, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="邮箱已注册")
    # 先不创建用户记录，待邮箱验证通过后创建
    code = generate_email_code()
    expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=5)
    db.add(EmailCode(email=payload.email, code_hash=_hash_code(code), purpose="register", expires_at=expires))
    db.commit()
    ok = send_email(
        db,
        to_email=payload.email,
        subject="注册验证码",
        content=f"<p>您的验证码是：<b>{code}</b>，5分钟内有效。</p>",
        purpose="register",
    )
    if not ok:
        raise HTTPException(status_code=500, detail="邮件发送失败")
    return {"message": "验证码已发送"}


@router.post("/verify-email")
@limiter.limit("10/minute")
def verify_email(request: Request, payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    record = (
        db.query(EmailCode)
        .filter(EmailCode.email == payload.email, EmailCode.purpose == "register", EmailCode.consumed == False)
        .order_by(EmailCode.id.desc())
        .first()
    )
    if not record or record.expires_at < now or record.code_hash != _hash_code(payload.code):
        raise HTTPException(status_code=400, detail="验证码无效或已过期")
    record.consumed = True
    # 创建用户
    user = User(email=payload.email, password_hash=hash_password(payload.password), is_verified=True)
    db.add(user)
    db.commit()
    return {"message": "注册成功"}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, payload: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="邮箱未验证")
    token = create_access_token(str(user.id))
    csrf = generate_csrf_token()
    # Cookie 设置
    response.set_cookie("access_token", token, httponly=True, secure=False, samesite="lax", max_age=settings.jwt_expire_delta.total_seconds())
    response.set_cookie("csrf_token", csrf, httponly=False, secure=False, samesite="lax")
    return TokenResponse(access_token=token, csrf_token=csrf)


@router.post("/request-password-reset")
@limiter.limit("5/minute")
def request_password_reset(request: Request, payload: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        # 防枚举：返回同样信息
        return {"message": "如果邮箱存在，我们已发送验证码"}
    code = generate_email_code()
    expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(minutes=5)
    db.add(EmailCode(email=payload.email, code_hash=_hash_code(code), purpose="reset", expires_at=expires))
    db.commit()
    send_email(db, payload.email, "重置密码验证码", f"<p>验证码：<b>{code}</b>，5分钟内有效。</p>", purpose="reset")
    return {"message": "如果邮箱存在，我们已发送验证码"}


@router.post("/verify-reset-code")
@limiter.limit("10/minute")
def verify_reset_code(request: Request, payload: VerifyResetCodeRequest, db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    record = (
        db.query(EmailCode)
        .filter(EmailCode.email == payload.email, EmailCode.purpose == "reset", EmailCode.consumed == False)
        .order_by(EmailCode.id.desc())
        .first()
    )
    if not record or record.expires_at < now or record.code_hash != _hash_code(payload.code):
        raise HTTPException(status_code=400, detail="验证码无效或已过期")
    record.consumed = True
    db.commit()
    return {"message": "验证码有效，可重置密码"}


@router.post("/reset-password")
@limiter.limit("5/minute")
def reset_password(request: Request, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    # 简化：根据 Cookie 中 access_token 提取用户
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
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "密码已重置"}