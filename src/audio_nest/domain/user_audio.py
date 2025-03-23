from dataclasses import dataclass, field
from uuid import UUID, uuid4

from audio_nest.domain.audio import Audio


@dataclass
class UserAudio(Audio):
    user_id: UUID
    title: str = field(repr=False)
    artist: str | None = field(default=None, repr=False)
    id: UUID = field(default_factory=uuid4)
