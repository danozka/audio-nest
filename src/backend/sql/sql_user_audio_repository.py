import logging
from logging import Logger
from pathlib import Path
from typing import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.domain.user_audio import UserAudio
from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from sql.domain.sql_audio import SqlAudio
from sql.domain.sql_user_audio import SqlUserAudio


class SqlUserAudioRepository(IUserAudioRepository):
    _log: Logger = logging.getLogger(__name__)
    _sql_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, sql_session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._sql_session_maker = sql_session_maker

    async def add_user_audio(self, user_audio: UserAudio) -> None:
        self._log.debug(f'Adding {user_audio}...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            async with session.begin():
                if not await session.get(entity=SqlAudio, ident=user_audio.source_id):
                    sql_audio: SqlAudio = SqlAudio(
                        source_id=user_audio.source_id,
                        file_path=str(user_audio.file_path),
                        bit_rate_kbps=user_audio.bit_rate_kbps,
                        codec=str(user_audio.codec)
                    )
                    session.add(sql_audio)
                session.add(
                    SqlUserAudio(
                        id=str(user_audio.id),
                        user_id=str(user_audio.user_id),
                        audio_name=user_audio.audio_name,
                        source_id=user_audio.source_id
                    )
                )
        self._log.debug(f'{user_audio} added')

    async def get_user_audio_from_source(self, source_id: str) -> UserAudio | None:
        self._log.debug(f'Getting user audio from source \'{source_id}\'...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_user_audio: SqlUserAudio | None = (
                await session.scalars(select(SqlUserAudio).where(SqlUserAudio.source_id == source_id))
            ).first()
        user_audio: UserAudio | None = None
        if sql_user_audio:
            user_audio = UserAudio(
                id=UUID(sql_user_audio.id),
                user_id=UUID(sql_user_audio.user_id),
                audio_name=sql_user_audio.audio_name,
                source_id=sql_user_audio.source_id,
                file_path=Path(sql_user_audio.audio.file_path),
                bit_rate_kbps=sql_user_audio.audio.bit_rate_kbps,
                codec=AudioCodec(sql_user_audio.audio.codec)
            )
        self._log.debug(f'User audio from source \'{source_id}\' retrieved')
        return user_audio

    async def get_user_audio_list(self, user_id: UUID) -> list[UserAudio]:
        self._log.debug(f'Getting user audio list for user \'{user_id}\'...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_user_audio_list: Sequence[SqlUserAudio] = (
                await session.scalars(select(SqlUserAudio).where(SqlUserAudio.user_id == str(user_id)))
            ).all()
        user_audio_list: list[UserAudio] = []
        sql_user_audio: SqlUserAudio
        for sql_user_audio in sql_user_audio_list:
            user_audio_list.append(
                UserAudio(
                    id=UUID(sql_user_audio.id),
                    user_id=UUID(sql_user_audio.user_id),
                    audio_name=sql_user_audio.audio_name,
                    source_id=sql_user_audio.source_id,
                    file_path=Path(sql_user_audio.audio.file_path),
                    bit_rate_kbps=sql_user_audio.audio.bit_rate_kbps,
                    codec=AudioCodec(sql_user_audio.audio.codec)
                )
            )
        self._log.debug(f'User audio list for user \'{user_id}\' retrieved')
        return user_audio_list

    async def get_user_audio(self, user_audio_id: UUID) -> UserAudio | None:
        self._log.debug(f'Getting user audio \'{user_audio_id}\'...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_user_audio: SqlUserAudio | None = await session.get(entity=SqlUserAudio, ident=str(user_audio_id))
        user_audio: UserAudio | None = None
        if sql_user_audio:
            user_audio = UserAudio(
                id=UUID(sql_user_audio.id),
                user_id=UUID(sql_user_audio.user_id),
                audio_name=sql_user_audio.audio_name,
                source_id=sql_user_audio.source_id,
                file_path=Path(sql_user_audio.audio.file_path),
                bit_rate_kbps=sql_user_audio.audio.bit_rate_kbps,
                codec=AudioCodec(sql_user_audio.audio.codec)
            )
        self._log.debug(f'User audio \'{user_audio_id}\' retrieved')
        return user_audio

    async def delete_user_audio(self, user_audio_id: UUID) -> None:
        self._log.debug(f'Deleting user audio \'{user_audio_id}\'...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            async with session.begin():
                sql_user_audio: SqlUserAudio | None = await session.get(entity=SqlUserAudio, ident=str(user_audio_id))
                if not sql_user_audio:
                    self._log.debug(f'User audio \'{user_audio_id}\' not found')
                    return
                await session.delete(sql_user_audio)
        self._log.debug(f'User audio \'{user_audio_id}\' deleted')

