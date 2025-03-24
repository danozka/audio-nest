import asyncio
import logging
from logging import Logger
from typing import TypeAlias

from youtube_search import YoutubeSearch

from audio_nest.services.i_audio_sources_repository import IAudioSourcesRepository
from audio_nest.domain.audio_source import AudioSource


YoutubeVideo: TypeAlias = dict[str, str | list[str]]


class YoutubeAudioSourcesRepository(IAudioSourcesRepository):
    _log: Logger = logging.getLogger(__name__)
    _max_results: int

    def __init__(self, max_results: int = 20) -> None:
        self._max_results = max_results

    async def get_audio_sources(self, search_query: str) -> list[AudioSource]:
        self._log.debug(f'Getting YouTube videos for search query \'{search_query}\'...')
        result: list[AudioSource] = []
        youtube_videos: list[YoutubeVideo] = (
            await asyncio.to_thread(YoutubeSearch, search_terms=search_query, max_results=self._max_results)
        ).to_dict()
        youtube_video: YoutubeVideo
        for youtube_video in youtube_videos:
            result.append(
                AudioSource(
                    id=youtube_video['id'],
                    name=youtube_video['title'],
                    thumbnail_url=youtube_video['thumbnails'][0]
                )
            )
        self._log.debug(f'YouTube videos for search query \'{search_query}\' retrieved')
        return result
