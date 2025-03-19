import asyncio
import logging
from logging import Logger
from typing import TypeAlias

from youtube_search import YoutubeSearch

from audio_nest.domain.video import Video
from audio_nest.repositories.i_videos_repository import IVideosRepository


YoutubeVideo: TypeAlias = dict[str, str | list[str]]


class YoutubeVideosRepository(IVideosRepository):
    _log: Logger = logging.getLogger(__name__)
    _max_results: int

    def __init__(self, max_results: int = 20) -> None:
        self._max_results = max_results

    async def get_videos(self, search_query: str) -> list[Video]:
        self._log.debug(f'Getting videos for search query \'{search_query}\'...')
        result: list[Video] = []
        youtube_videos: list[YoutubeVideo] = (
            await asyncio.to_thread(YoutubeSearch, search_terms=search_query, max_results=self._max_results)
        ).to_dict()
        youtube_video: YoutubeVideo
        for youtube_video in youtube_videos:
            result.append(
                Video(
                    id=youtube_video['id'],
                    title=youtube_video['title'],
                    thumbnail_url=youtube_video['thumbnails'][0]
                )
            )
        self._log.debug(f'Videos for search query \'{search_query}\' retrieved')
        return result
