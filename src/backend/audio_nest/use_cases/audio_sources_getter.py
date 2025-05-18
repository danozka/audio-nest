import logging
from logging import Logger

from audio_nest.services.i_audio_sources_repository import IAudioSourcesRepository
from audio_nest.domain.audio_source import AudioSource


class AudioSourcesGetter:
    _log: Logger = logging.getLogger(__name__)
    _audio_sources_repository: IAudioSourcesRepository

    def __init__(self, audio_sources_repository: IAudioSourcesRepository) -> None:
        self._audio_sources_repository = audio_sources_repository

    async def get_audio_sources(self, search_query: str) -> list[AudioSource]:
        self._log.debug(f'Getting audio sources for search query \'{search_query}\'...')
        result: list[AudioSource] = await self._audio_sources_repository.get_audio_sources(search_query)
        self._log.debug(f'Audio sources for search query \'{search_query}\' retrieved')
        return result
