from dataclasses import dataclass, field


@dataclass
class AudioSource:
    id: str
    name: str = field(repr=False)
    thumbnail_url: str | None = field(default=None, repr=False)
