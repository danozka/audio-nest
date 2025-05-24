from api.dtos.base_dto import BaseDto


class AudioSourceDto(BaseDto):
    id: str
    name: str
    thumbnail_url: str | None = None
