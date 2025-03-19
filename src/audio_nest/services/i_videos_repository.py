from abc import ABC, abstractmethod

from audio_nest.domain.video import Video


class IVideosRepository(ABC):
    @abstractmethod
    async def get_videos(self, search_query: str) -> list[Video]:
        raise NotImplementedError
