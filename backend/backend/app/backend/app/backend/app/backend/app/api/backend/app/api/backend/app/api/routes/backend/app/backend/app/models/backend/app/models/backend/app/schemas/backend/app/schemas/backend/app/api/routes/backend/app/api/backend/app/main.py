
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

# Import models so SQLAlchemy registers all tables
from app.models import User, WalletAccount

from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    # Development database initialization
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Educational Virtual Game Simulation Platform",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=[
        "Authorization",
        "Content-Type",
        "Idempotency-Key"
    ]
)


app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)


@app.get("/")
async def root():

    return {
        "success": True,
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": "backend"
    }
  
