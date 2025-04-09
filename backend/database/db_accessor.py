import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

logger = logging.getLogger("database")


class DatabaseAccessor:
    """
    Класс для работы с SQLite базой данных через асинхронное подключение.
    Поддерживает миграции через Alembic.
    """

    def __init__(self, database_url: str):
        """
        Args:
            database_url: URL для подключения к SQLite, например 'sqlite+aiosqlite:///./database.db'
        """
        self._database_url = database_url
        self._engine = None
        self._async_session_maker = None

    def run(self) -> None:
        """Инициализация подключения к базе данных"""
        self._engine = create_async_engine(
            self._database_url, connect_args={"check_same_thread": False}, echo=False
        )

        self._async_session_maker = sessionmaker(
            bind=self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def stop(self) -> None:
        """Закрытие соединения с базой данных"""
        if self._engine:
            await self._engine.dispose()

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Контекстный менеджер для получения сессии базы данных.

        Yields:
            AsyncSession: Асинхронная сессия SQLAlchemy
        """
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call .run() first")

        async with self._async_session_maker() as session:
            yield session

    async def init_db(self, Base: DeclarativeBase) -> None:
        """
        Создание всех таблиц в базе данных.
        Использовать только если не используется Alembic.

        Args:
            Base: Базовый класс моделей SQLAlchemy
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def check_connection(self) -> None:
        """Проверка подключения к базе данных"""
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
                logger.info("Successfully connected to SQLite database")
        except Exception as e:
            logger.error(f"Failed to connect to the database: {e}")
            raise

    def get_async_session_maker(self) -> sessionmaker:
        """
        Получение фабрики сессий для создания асинхронных сессий.

        Returns:
            sessionmaker: Фабрика для создания асинхронных сессий

        Raises:
            RuntimeError: Если база данных не была инициализирована
        """
        if not self._async_session_maker:
            raise RuntimeError("Database not initialized. Call .run() first")
        return self._async_session_maker
