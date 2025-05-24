from dataclasses import dataclass


@dataclass
class AudioSource:
    id: str
    name: str
    thumbnail_url: str | None = None
