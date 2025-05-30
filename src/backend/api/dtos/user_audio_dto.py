from uuid import UUID

from api.dtos.base_dto import BaseDto


class UserAudioDto(BaseDto):
    audio_name: str
    id: UUID | None = None
