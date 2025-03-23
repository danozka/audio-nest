from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.domain.user import User
from audio_nest.services.i_users_repository import IUsersRepository
from sql.domain.sql_user import SqlUser


class SqlUsersRepository(IUsersRepository):
    _sql_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, sql_session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._sql_session_maker = sql_session_maker

    async def get_user_by_email(self, email: str) -> User | None:
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_user: SqlUser | None = (await session.scalars(select(SqlUser).where(SqlUser.email == email))).first()
        result: User | None = None
        if sql_user:
            result = User(email=sql_user.email, hashed_password=sql_user.hashed_password, id=UUID(sql_user.id))
        return result

    async def create_user(self, user: User) -> None:
        session: AsyncSession
        async with self._sql_session_maker() as session:
            async with session.begin():
                session.add(SqlUser(id=str(user.id), email=user.email, hashed_password=user.hashed_password))
