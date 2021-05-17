import sys
from os import pardir
from os import path

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

dir_path = path.dirname(path.abspath(__file__).replace("db", ""))
sys.path.append(path.abspath(path.join(dir_path, pardir)))

from app.api.router import api_router  # noqa: E402
from app.core.config import settings  # noqa: E402


app = FastAPI(title="Improvement API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_STR)
