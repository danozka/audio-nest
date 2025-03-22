from dataclasses import dataclass, field
from uuid import UUID, uuid4

from audio_nest.domain.user_audio import UserAudio


@dataclass
class User:
    email: str = field(repr=False)
    hashed_password: str = field(repr=False)
    id: UUID = field(default_factory=uuid4)
    audio_list: list[UserAudio] = field(default_factory=list, repr=False)
