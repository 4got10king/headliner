import io
import uuid
from typing import List
from urllib.parse import urlparse

import aiohttp
from PIL import Image

from app.schemas.image import ImageAction, ImageTaskRequest, ImageTaskResult
from config.mq import mq_settings
from mq.mq_context import MQContext


class ImageService:
    @classmethod
    async def download_image(cls, image_url: str) -> Image.Image:
        """Скачивание изображения по URL"""
        if not image_url:
            raise ValueError("Image URL is empty")

        parsed_url = urlparse(image_url)
        if not all([parsed_url.scheme, parsed_url.netloc]):
            raise ValueError(f"Invalid image URL: {image_url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    raise ValueError(f"Failed to download image from {image_url}")
                image_data = await response.read()
                return Image.open(io.BytesIO(image_data))

    @classmethod
    async def remove_background(cls, image: Image.Image) -> str:
        """Удаление фона изображения (имитация)"""
        storage_path = mq_settings.storage_path
        storage_path.mkdir(parents=True, exist_ok=True)
        output_path = storage_path / f"no_bg_{uuid.uuid4()}.png"
        image.save(output_path)
        return str(output_path)

    @classmethod
    async def generate_preview(cls, image: Image.Image, size: tuple[int, int] = (300, 300)) -> str:
        """Генерация превью изображения"""
        storage_path = mq_settings.storage_path
        storage_path.mkdir(parents=True, exist_ok=True)
        preview = image.resize(size, Image.Resampling.LANCZOS)
        output_path = storage_path / f"preview_{uuid.uuid4()}.png"
        preview.save(output_path)
        return str(output_path)

    @classmethod
    async def search_similar(cls, image: Image.Image) -> List[str]:
        """Поиск похожих изображений (имитация)"""
        return [f"image{i}.jpg" for i in range(1, 3)]

    @classmethod
    async def process_task(cls, task: ImageTaskRequest) -> ImageTaskResult:
        """Обработка задачи по обработке изображения"""
        try:
            image = await cls.download_image(task.image_url)
            result = None

            if task.action == ImageAction.REMOVE_BACKGROUND:
                result_path = await cls.remove_background(image)
                result = {"image_path": result_path}
            elif task.action == ImageAction.GENERATE_PREVIEW:
                result_path = await cls.generate_preview(image)
                result = {"preview_path": result_path}
            elif task.action == ImageAction.SEARCH_SIMILAR:
                similar_images = await cls.search_similar(image)
                result = {"similar_images": similar_images}
            else:
                raise ValueError(f"Unknown action: {task.action}")

            async with MQContext() as mq:
                await mq.publish_result(str(task.task_id), "success", result)

            return ImageTaskResult(task_id=task.task_id, status="success", result=result)
        except Exception as e:
            async with MQContext() as mq:
                await mq.publish_result(str(task.task_id), "error", {"error": str(e)})

            return ImageTaskResult(task_id=task.task_id, status="error", result={"error": str(e)})
