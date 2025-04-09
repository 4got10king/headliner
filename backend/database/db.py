from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from config.db import db_settings

from .db_accessor import DatabaseAccessor

database_accessor = DatabaseAccessor(database_url=db_settings.dsn_async)

database_accessor.run()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with database_accessor.get_session() as session:
        yield session
