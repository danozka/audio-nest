from abc import ABC, abstractmethod

from audio_nest.domain.audio_source import AudioSource


class IAudioSourcesRepository(ABC):
    @abstractmethod
    async def get_audio_sources(self, search_query: str) -> list[AudioSource]:
        raise NotImplementedError
