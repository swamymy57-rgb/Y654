from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.api.router import api_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Educational Virtual Game Simulation Platform"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type", "Idempotency-Key"],
)


app.include_router(
    api_router,
    prefix=settings.API_PREFIX
)


@app.get("/")
async def root():

    return {
        "success": True,
        "message": "Virtual Game Simulation Platform Backend",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():

    return {
        "status": "healthy",
        "service": "backend"
    }
