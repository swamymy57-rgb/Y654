from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():

    return {
        "success": True,
        "service": "Game Platform API",
        "status": "online"
    }


@router.get("/version")
async def version():

    return {
        "version": "1.0.0",
        "api_version": "v1"
    }


@router.get("/status")
async def system_status():

    return {
        "backend": "online",
        "database": "not_connected_yet",
        "redis": "not_connected_yet",
        "mode": "virtual_simulation"
    }
