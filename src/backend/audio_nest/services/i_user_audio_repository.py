from abc import ABC, abstractmethod
from uuid import UUID

from audio_nest.domain.user_audio import UserAudio


class IUserAudioRepository(ABC):
    @abstractmethod
    async def add_user_audio(self, user_audio: UserAudio) -> None:
        pass

    @abstractmethod
    async def get_user_audio_from_source(self, source_id: str) -> UserAudio | None:
        pass

    @abstractmethod
    async def get_user_audio_list(self, user_id: UUID) -> list[UserAudio]:
        pass

    @abstractmethod
    async def get_user_audio(self, user_audio_id: UUID) -> UserAudio | None:
        pass

    @abstractmethod
    async def delete_user_audio(self, user_audio_id: UUID) -> None:
        pass
