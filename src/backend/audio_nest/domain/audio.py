from dataclasses import dataclass
from pathlib import Path

from audio_nest.domain.audio_codec import AudioCodec


@dataclass
class Audio:
    source_id: str
    file_path: Path
    bit_rate_kbps: int
    codec: AudioCodec
