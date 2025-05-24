import logging
from logging import Logger

from api.dtos.audio_source_dto import AudioSourceDto
from audio_nest.domain.audio_source import AudioSource


class AudioSourcesAdapter:
    _log: Logger = logging.getLogger(__name__)

    def adapt_audio_sources(self, audio_sources: list[AudioSource]) -> list[AudioSourceDto]:
        self._log.debug(f'Adapting {audio_sources}...')
        result: list[AudioSourceDto] = [AudioSourceDto.model_validate(x.__dict__) for x in audio_sources]
        self._log.debug(f'{audio_sources} adapted')
        return result
