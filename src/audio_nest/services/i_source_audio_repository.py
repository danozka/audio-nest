from abc import ABC, abstractmethod

from audio_nest.domain.audio import Audio


class ISourceAudioRepository(ABC):
    @abstractmethod
    async def get_audio_from_source(self, source_id: str) -> Audio:
        raise NotImplementedError
