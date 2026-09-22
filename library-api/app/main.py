from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.database import init_db
from app.api.v1.endpoints import books

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0",
    description="API for managing a virtual library",
    lifespan=lifespan
)

app.include_router(books.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy"}
