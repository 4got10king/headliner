from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ImageAction(str, Enum):
    REMOVE_BACKGROUND = "remove_background"
    GENERATE_PREVIEW = "generate_preview"
    SEARCH_SIMILAR = "search_similar"


class ImageTaskRequest(BaseModel):
    """Схема входящего сообщения из очереди"""

    task_id: UUID = Field(..., description="Уникальный идентификатор задачи")
    action: ImageAction = Field(
        ..., description="Тип действия для обработки изображения"
    )
    image_url: str = Field(..., description="URL изображения для обработки")


class ImageTaskResult(BaseModel):
    """Схема результата обработки изображения"""

    task_id: UUID = Field(..., description="Уникальный идентификатор задачи")
    status: str = Field(..., description="Статус выполнения задачи")
    result: dict[str, Any] = Field(..., description="Результат обработки изображения")
