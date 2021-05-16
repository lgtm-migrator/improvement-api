import secrets
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings


load_dotenv()


# The pydantic BaseSettings model lets you define settings
# that can have default values and values defined in .env
# will override them
class Settings(BaseSettings):
    API_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    ALGORITHM: str = "HS256"

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str]

    class Config:
        case_sensitive = True


settings = Settings()
