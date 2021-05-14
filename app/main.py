import sys
from os import pardir
from os import path

import uvicorn
from fastapi import FastAPI

dir_path = path.dirname(path.abspath(__file__).replace("db", ""))
sys.path.append(path.abspath(path.join(dir_path, pardir)))

from app.api.router import api_router  # noqa: E402
from app.core.config import settings  # noqa: E402


app = FastAPI(title="Improvement API")


app.include_router(api_router, prefix=settings.API_STR)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, host="localhost")
