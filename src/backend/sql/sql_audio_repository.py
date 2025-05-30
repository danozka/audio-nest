import logging
from logging import Logger
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from audio_nest.domain.audio import Audio
from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.services.i_audio_repository import IAudioRepository
from sql.domain.sql_audio import SqlAudio


class SqlAudioRepository(IAudioRepository):
    _log: Logger = logging.getLogger(__name__)
    _sql_session_maker: async_sessionmaker[AsyncSession]

    def __init__(self, sql_session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._sql_session_maker = sql_session_maker

    async def get_audio_from_source(self, source_id: str) -> Audio | None:
        self._log.debug(f'Getting audio from source \'{source_id}\'...')
        session: AsyncSession
        async with self._sql_session_maker() as session:
            sql_audio: SqlAudio | None = await session.get(entity=SqlAudio, ident=source_id)
        audio: Audio | None = None
        if sql_audio:
            audio = Audio(
                source_id=sql_audio.source_id,
                file_path=Path(sql_audio.file_path),
                bit_rate_kbps=sql_audio.bit_rate_kbps,
                codec=AudioCodec(sql_audio.codec)
            )
        self._log.debug(f'Audio from source \'{source_id}\' retrieved')
        return audio
