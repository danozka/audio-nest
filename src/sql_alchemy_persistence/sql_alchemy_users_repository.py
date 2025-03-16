from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.domain.user import User
from audio_nest.persistence.i_users_repository import IUsersRepository
from sql_alchemy_persistence.domain.sql_alchemy_user import SqlAlchemyUser


class SqlAlchemyUsersRepository(IUsersRepository):
    _session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker

    async def get_user_by_email(self, email: str) -> User | None:
        session: AsyncSession
        async with self._session_maker() as session:
            return (await session.scalars(select(SqlAlchemyUser).where(SqlAlchemyUser.email == email))).first()

    async def create_user(self, user: User) -> None:
        session: AsyncSession
        async with self._session_maker() as session:
            async with session.begin():
                session.add(SqlAlchemyUser(id=str(user.id), email=user.email, hashed_password=user.hashed_password))
