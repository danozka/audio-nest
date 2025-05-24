from dataclasses import dataclass
from uuid import UUID

from audio_nest.domain.audio import Audio


@dataclass
class UserAudio(Audio):
    id: UUID
    user_id: UUID
    audio_name: str
