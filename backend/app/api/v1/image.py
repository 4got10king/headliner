from fastapi import APIRouter

from app.schemas.image import ImageTaskRequest, ImageTaskResult
from app.service.image import ImageService

router = APIRouter(prefix="/image", tags=["01 Image Processing Tasks"])


@router.post("/", response_model=ImageTaskResult)
async def create_image_task(task: ImageTaskRequest) -> ImageTaskResult:
    """Создание новой задачи обработки изображения"""
    return await ImageService.process_task(task)
