from pydantic import Field

from api.dtos.base_dto import BaseDto


class AudioSourceDto(BaseDto):
    id: str
    name: str = Field(repr=False)
    thumbnail_url: str | None = Field(default=None, repr=False)
