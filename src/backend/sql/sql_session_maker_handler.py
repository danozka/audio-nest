import logging
from logging import Logger
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncConnection, AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from sql.domain.sql_base import SqlBase


log: Logger = logging.getLogger(__name__)


async def handle_sql_session_maker(database_path: Path) -> AsyncGenerator[async_sessionmaker[AsyncSession], None]:
    log.debug('Initializing SQL session maker...')
    database_path.parent.mkdir(parents=True, exist_ok=True)
    engine: AsyncEngine = create_async_engine(f'sqlite+aiosqlite:///{database_path.resolve()}')
    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(bind=engine, expire_on_commit=False)
    connection: AsyncConnection
    async with engine.begin() as connection:
        await connection.run_sync(SqlBase.metadata.create_all)
    log.debug('SQL session maker initialized')
    yield session_maker
    log.debug('Closing SQL session maker...')
    await engine.dispose()
    log.debug('SQL session maker closed')
