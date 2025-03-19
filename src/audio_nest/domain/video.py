from dataclasses import dataclass, field


@dataclass
class Video:
    id: str
    thumbnail_url: str = field(repr=False)
    title: str = field(repr=False)
