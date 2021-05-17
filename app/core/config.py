import secrets
from typing import List
from typing import Optional
from typing import Union

from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import Field
from pydantic import validator


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

    DATABASE_URL: str
    TEST_DATABASE_URL: Optional[str]

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = Field(..., env="BACKEND_CORS_ORIGINS")

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True


settings = Settings()
