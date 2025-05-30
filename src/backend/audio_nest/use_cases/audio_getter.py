import logging
from logging import Logger

from audio_nest.services.i_audio_downloader import IAudioDownloader
from audio_nest.services.i_audio_repository import IAudioRepository
from audio_nest.domain.user_audio import Audio


class AudioGetter:
    _log: Logger = logging.getLogger(__name__)
    _audio_downloader: IAudioDownloader
    _audio_repository: IAudioRepository

    def __init__(self, audio_downloader: IAudioDownloader, audio_repository: IAudioRepository) -> None:
        self._audio_downloader = audio_downloader
        self._audio_repository = audio_repository

    async def get_audio_from_source(self, source_id: str) -> Audio:
        self._log.debug(f'Getting audio from source \'{source_id}\'...')
        audio: Audio = (
            await self._audio_repository.get_audio_from_source(source_id) or
            await self._audio_downloader.download_audio_from_source(source_id)
        )
        self._log.debug(f'Audio from source \'{source_id}\' retrieved')
        return audio
