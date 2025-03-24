from abc import ABC, abstractmethod

from audio_nest.domain.user_audio import UserAudio


class IUserAudioRepository(ABC):
    @abstractmethod
    async def add_user_audio(self, user_audio: UserAudio) -> None:
        raise NotImplementedError

    @abstractmethod
    async def get_user_audio_from_source(self, source_id: str) -> UserAudio:
        raise NotImplementedError
