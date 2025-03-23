from uuid import UUID, uuid4

from pydantic import Field

from api.dtos.base_dto import BaseDto


class UserAudioDto(BaseDto):
    title: str = Field(repr=False)
    artist: str | None = Field(default=None, repr=False)
    id: UUID = Field(default_factory=uuid4)
