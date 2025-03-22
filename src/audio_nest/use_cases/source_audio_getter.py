import logging
from logging import Logger

from audio_nest.services.i_source_audio_repository import ISourceAudioRepository
from audio_nest.domain.user_audio import Audio


class SourceAudioGetter:
    _log: Logger = logging.getLogger(__name__)
    _source_audio_repository: ISourceAudioRepository

    def __init__(self, source_audio_repository: ISourceAudioRepository) -> None:
        self._source_audio_repository = source_audio_repository

    async def get_audio_from_source(self, source_id: str) -> Audio:
        self._log.debug(f'Getting audio with source ID \'{source_id}\'...')
        result: Audio = await self._source_audio_repository.get_audio_from_source(source_id)
        self._log.debug(f'Audio with source ID \'{source_id}\' retrieved')
        return result
