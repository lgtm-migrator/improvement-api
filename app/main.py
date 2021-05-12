import uvicorn
from fastapi import FastAPI

from app.api.router import api_router

from dotenv import load_dotenv

load_dotenv()


app = FastAPI(
    title="Improvement API"
)


app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, host="localhost")
