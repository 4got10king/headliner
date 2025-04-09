from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MQSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="RABBITMQ_",
    )

    """
    Настройки подключения к RabbitMQ.
    """

    USER: str = "guest"
    PASSWORD: str = "guest"
    HOST: str = "localhost"
    PORT: int = 5672
    VHOST: str = "/"
    STORAGE_PATH: str = "storage/images"

    @computed_field(return_type=str)
    def url(self) -> str:
        """URL для подключения к RabbitMQ"""
        return f"amqp://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}{self.VHOST}"

    @computed_field(return_type=Path)
    def storage_path(self) -> Path:
        """Полный путь к директории для хранения изображений"""
        return Path(__file__).resolve().parent.parent.parent / self.STORAGE_PATH


mq_settings = MQSettings()
