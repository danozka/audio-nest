from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID, uuid4

from audio_nest.domain.audio_codec import AudioCodec


@dataclass
class Audio:
    file_path: Path = field(repr=False)
    title: str = field(repr=False)
    artist: str = field(repr=False)
    codec: AudioCodec = field(repr=False)
    bit_rate_kbps: int = field(repr=False)
    source_id: str = field(repr=False)
    user_id: UUID = field(repr=False)
    id: UUID = field(default_factory=uuid4)
