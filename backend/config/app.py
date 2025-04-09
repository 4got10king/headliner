from pathlib import Path
from typing import List

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """
    Конфигурационные настройки приложения.

    Класс загружает настройки из .env файла в корневой директории проекта.
    Все переменные окружения должны иметь префикс BACKEND_SERVER__.

    Attributes:
        PORT (int): Порт, на котором будет запущен сервер
        HOST (str): Хост для запуска сервера
        WORKERS (int): Количество рабочих процессов
        METHODS (List[str]): Разрешенные HTTP методы
        HEADERS (List[str]): Разрешенные HTTP заголовки
        origins (List[str]): Разрешенные источники для CORS (по умолчанию ["*"])

    Properties:
        app_settings: Возвращает экземпляр текущих настроек
        swagger_conf: Конфигурация для Swagger/OpenAPI документации
        server_url: URL сервера в формате http://{HOST}:{PORT}

    Example:
        Пример переменных в .env файле:
        BACKEND_SERVER__PORT=8000
        BACKEND_SERVER__HOST=localhost
        BACKEND_SERVER__WORKERS=4
    """

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_prefix="BACKEND_SERVER__",
    )
    PORT: int
    HOST: str
    WORKERS: int
    METHODS: List[str]
    HEADERS: List[str]
    origins: List[str] = ["*"]

    @property
    def app_settings(self):
        return self

    @property
    def swagger_conf(self) -> dict:
        return dict(
            version="0.0.1",
            description="HEADLINER REST API",
            title="headliner",
            docs_url="/swagger",
            openapi_url="/api/openapi.json",
        )

    @computed_field(return_type=str)
    @property
    def server_url(self) -> str:
        return f"http://{self.PORT}:{self.PORT}"


app_config = AppSettings()
