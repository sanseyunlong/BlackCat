import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.config import settings
from app.routes import auth as auth_routes
from app.routes import users as users_routes
from app.routes import images as images_routes
from app.routes import recognitions as rec_routes
from app.routes import records as records_routes
from fastapi import APIRouter
from app.routes.middleware import csrf_middleware
from app.services.rate_limit import limiter


app = FastAPI(title=settings.app_name)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, lambda request, exc: exc)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(csrf_middleware)

api_router = APIRouter(prefix="/api")
api_router.include_router(auth_routes.router)
api_router.include_router(users_routes.router)
api_router.include_router(images_routes.router)
api_router.include_router(rec_routes.router)
api_router.include_router(records_routes.router)
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.backend_port)