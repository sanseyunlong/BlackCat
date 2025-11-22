import os
from datetime import timedelta
from pydantic import BaseModel
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Settings(BaseModel):
    model_config = {"protected_namespaces": ()}
    
    app_name: str = "BlackCat AI"
    backend_port: int = int(os.getenv("BACKEND_PORT", "8000"))

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///data/app.db")

    jwt_secret: str = os.getenv("JWT_SECRET", "change-this-in-prod")
    jwt_expire_days: int = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.163.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "465"))
    sender_email: str = os.getenv("SENDER_EMAIL", "chaohubai@163.com")
    sender_password: str = os.getenv("SENDER_PASSWORD", "")

    frontend_origin: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    siliconflow_api_key: str = os.getenv("SILICONFLOW_API_KEY", "")
    siliconflow_base_url: str = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn")
    model_name: str = os.getenv("MODEL_NAME", "generic-image-classifier")

    @property
    def jwt_expire_delta(self) -> timedelta:
        return timedelta(days=self.jwt_expire_days)


settings = Settings()