import os
import secrets
from typing import List
from dotenv import load_dotenv

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
root_dir = os.path.abspath(os.path.join(backend_dir, ".."))
env_path = os.path.join(root_dir, ".env")
if os.path.isfile(env_path):
    load_dotenv(env_path)


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_cors_origins(value: str) -> List[str]:
    origins = [origin.strip().rstrip("/") for origin in value.split(",") if origin.strip()]
    if not origins:
        raise ValueError("CORS_ORIGINS must include at least one origin.")
    if "*" in origins:
        raise ValueError("CORS_ORIGINS must not contain '*'. Configure explicit origins instead.")
    return origins


class Settings:
    """
    Environment-backed application configuration system with strict production validation.
    Supports development, test, and production environments.
    """

    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
        if self.APP_ENV not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production.")

        demo_default = "true" if self.APP_ENV == "development" else "false"
        self.DEMO_MODE = _parse_bool(os.getenv("DEMO_MODE", demo_default))
        if self.APP_ENV == "production" and self.DEMO_MODE:
            raise ValueError("DEMO_MODE cannot be enabled in production.")

        configured_secret = os.getenv("JWT_SECRET_KEY", "").strip()
        if not configured_secret:
            configured_secret = "campusmind_prod_secret_key_jwt_authentication_2026_secure_token_999"
        self.JWT_SECRET_KEY = configured_secret
        self.JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))

        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

        self.DEMO_PASSWORD = os.getenv("DEMO_PASSWORD", "password123")
        self.EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "sentence-transformers")
        self.EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

        self.CHROMA_DB_DIR = self._resolve_path(os.getenv("CHROMA_DB_DIR", "./backend/chroma_db"))
        self.DATABASE_URL = self._resolve_database_url(
            os.getenv("DATABASE_URL", "sqlite:///./backend/campusmind.db")
        )
        self.DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
        self.DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
        self.DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))
        self.DB_POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", "1800"))
        self.DB_POOL_PRE_PING = _parse_bool(os.getenv("DB_POOL_PRE_PING", "true"))

        self.TASK_QUEUE_PROVIDER = os.getenv("TASK_QUEUE_PROVIDER", "threaded").strip().lower()
        self.REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0").strip()
        self.NOTIFICATION_TRANSPORT = os.getenv("NOTIFICATION_TRANSPORT", "sse").strip().lower()

        self.RETRIEVAL_TOP_K = int(os.getenv("RETRIEVAL_TOP_K", "5"))
        self.SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.25"))
        self.RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.API_V1_PREFIX = "/api/v1"

        configured_origins = os.getenv("CORS_ORIGINS")
        if not configured_origins:
            configured_origins = "http://localhost:5173,http://localhost:3000,http://localhost:8000,https://onrender.com"
        self.CORS_ORIGINS = parse_cors_origins(configured_origins)

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == "development"

    @property
    def is_test(self) -> bool:
        return self.APP_ENV == "test"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    @staticmethod
    def _resolve_path(value: str) -> str:
        if os.path.isabs(value):
            return value
        return os.path.abspath(os.path.join(root_dir, value.lstrip("./")))

    @staticmethod
    def _resolve_database_url(value: str) -> str:
        if value.startswith("postgres://"):
            value = value.replace("postgres://", "postgresql://", 1)
        if not value.startswith("sqlite:///"):
            return value
        db_path = value.replace("sqlite:///", "", 1)
        if os.path.isabs(db_path):
            return value
        return f"sqlite:///{os.path.abspath(os.path.join(root_dir, db_path.lstrip('./')))}"


settings = Settings()
