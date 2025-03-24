from dataclasses import dataclass, field
from pathlib import Path

from audio_nest.domain.audio_codec import AudioCodec


@dataclass
class Audio:
    source_id: str
    file_path: Path = field(repr=False)
    bit_rate_kbps: int = field(repr=False)
    codec: AudioCodec = field(repr=False)
