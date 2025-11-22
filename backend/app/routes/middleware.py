from fastapi import Request, Response
from fastapi import status


async def csrf_middleware(request: Request, call_next):
    # 仅校验非幂等敏感方法
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        # 放行登录、验证码、图片上传和识别相关接口（这些接口已有登录验证）
        if (request.url.path.startswith("/api/auth/") or 
            request.url.path.startswith("/api/images") or 
            request.url.path.startswith("/api/recognitions")):
            return await call_next(request)
        csrf_header = request.headers.get("X-CSRF-Token")
        csrf_cookie = request.cookies.get("csrf_token")
        if not csrf_header or not csrf_cookie or csrf_header != csrf_cookie:
            return Response(status_code=status.HTTP_403_FORBIDDEN, content="CSRF token invalid")
    return await call_next(request)