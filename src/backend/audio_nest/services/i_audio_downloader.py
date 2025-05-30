from abc import ABC, abstractmethod

from audio_nest.domain.user_audio import Audio


class IAudioDownloader(ABC):
    @abstractmethod
    async def download_audio_from_source(self, source_id: str) -> Audio:
        pass
