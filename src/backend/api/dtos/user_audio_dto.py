from uuid import UUID, uuid4

from pydantic import Field

from api.dtos.base_dto import BaseDto


class UserAudioDto(BaseDto):
    audio_name: str
    id: UUID = Field(default_factory=uuid4)
