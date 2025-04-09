from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["00 HEALTH"])


@router.get("/")
async def health_check():
    """Проверка работоспособности сервиса"""
    return {"status": "ok"}
