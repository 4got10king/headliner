from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings


class DBSettings(BaseSettings):
    """
    Настройки подключения к SQLite базе данных.
    """

    NAME: str = "database.db"

    @property
    def db_path(self) -> Path:
        """Полный путь к файлу базы данных"""
        return Path(__file__).resolve().parent.parent.parent / self.NAME

    @computed_field(return_type=str)
    def dsn_async(self) -> str:
        """URL для асинхронного подключения к SQLite"""
        return f"sqlite+aiosqlite:///{self.db_path}"

    @computed_field(return_type=str)
    def db_url_for_cli(self) -> str:
        """URL для использования в командной строке (например, для Alembic)"""
        return f"sqlite:///{self.db_path}"


class TestDBSettings(DBSettings):
    """
    Настройки для тестовой базы данных.
    Использует отдельный файл базы данных для тестов.
    """

    NAME: str = ":memory:"


db_settings = DBSettings()
test_db_settings = TestDBSettings()
