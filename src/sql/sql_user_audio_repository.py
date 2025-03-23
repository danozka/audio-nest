from pathlib import Path
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.domain.user_audio import UserAudio
from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from sql.domain.sql_user_audio import SqlUserAudio


class SqlUserAudioRepository(IUserAudioRepository):
    _sql_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, sql_session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._sql_session_maker = sql_session_maker

    async def add_user_audio(self, user_audio: UserAudio) -> None:
        session: AsyncSession
        async with self._sql_session_maker() as session:
            async with session.begin():
                session.add(
                    SqlUserAudio(
                        id=str(user_audio.id),
                        user_id=str(user_audio.user_id),
                        title=user_audio.title,
                        artist=user_audio.artist,
                        source_id=user_audio.source_id,
                        file_path=str(user_audio.file_path),
                        bit_rate_kbps=user_audio.bit_rate_kbps,
                        codec=user_audio.codec
                    )
                )

    async def get_user_audio_from_source(self, source_id: str) -> UserAudio | None:
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_user_audio: SqlUserAudio | None = (
                await session.scalars(select(SqlUserAudio).where(SqlUserAudio.source_id == source_id))
            ).first()
        result: UserAudio | None = None
        if sql_user_audio:
            result = UserAudio(
                id=UUID(sql_user_audio.id),
                user_id=UUID(sql_user_audio.user_id),
                title=sql_user_audio.title,
                artist=sql_user_audio.artist,
                source_id=sql_user_audio.source_id,
                file_path=Path(sql_user_audio.file_path),
                bit_rate_kbps=sql_user_audio.bit_rate_kbps,
                codec=AudioCodec(sql_user_audio.codec)
            )
        return result
