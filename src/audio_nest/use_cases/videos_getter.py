import logging
from logging import Logger

from audio_nest.services.i_videos_repository import IVideosRepository
from audio_nest.domain.video import Video


class VideosGetter:
    _log: Logger = logging.getLogger(__name__)
    _videos_repository: IVideosRepository

    def __init__(self, videos_repository: IVideosRepository) -> None:
        self._videos_repository = videos_repository

    async def get_videos(self, search_query: str) -> list[Video]:
        self._log.debug(f'Getting videos for search query \'{search_query}\'...')
        result: list[Video] = await self._videos_repository.get_videos(search_query)
        self._log.debug(f'Videos for search query \'{search_query}\' retrieved')
        return result
