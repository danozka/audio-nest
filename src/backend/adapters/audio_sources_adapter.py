import logging
from logging import Logger

from api.dtos.audio_source_dto import AudioSourceDto
from audio_nest.domain.audio_source import AudioSource


class AudioSourcesAdapter:
    _log: Logger = logging.getLogger(__name__)

    def adapt_audio_sources(self, audio_sources: list[AudioSource]) -> list[AudioSourceDto]:
        self._log.debug('Adapting audio sources...')
        result: list[AudioSourceDto] = [
            AudioSourceDto(
                id=audio_source.id,
                name=audio_source.name,
                thumbnail_url=audio_source.thumbnail_url
            )
            for audio_source in audio_sources
        ]
        self._log.debug('Audio sources adapted')
        return result
