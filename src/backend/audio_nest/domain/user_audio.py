from dataclasses import dataclass, field
from uuid import UUID

from audio_nest.domain.audio import Audio


@dataclass
class UserAudio(Audio):
    id: UUID
    user_id: UUID
    title: str = field(repr=False)
    artist: str | None = field(default=None, repr=False)
