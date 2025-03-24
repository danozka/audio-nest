from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings

from audio_nest.domain.audio_codec import AudioCodec


class Settings(BaseSettings):
    app_host: str = Field(alias='APP_HOST', default='0.0.0.0')
    app_port: int = Field(alias='APP_HOST', default=8000)
    audio_bit_rate_kbps: int = Field(alias='AUDIO_BIT_RATE_KBPS', default=320)
    audio_codec: AudioCodec = Field(alias='AUDIO_CODEC', default=AudioCodec.vorbis)
    audio_directory_path: Path = Field(alias='AUDIO_DIRECTORY_PATH', default=Path('./data/audio'))
    database_path: Path = Field(alias='DATABASE_PATH', default=Path('./data/audio-nest.db'))
    ffmpeg_path: Path = Field(alias='FFMPEG_PATH', default=Path('.'))
    json_web_token_secret_key: str = Field(alias='JWT_SECRET_KEY', default='my_secret_key')
    json_web_token_algorithm: str = Field(alias='JWT_ALGORITHM', default='HS256')
    json_web_token_expiration_days: int = Field(alias='JWT_ACCESS_TOKEN_EXPIRATION_DAYS', default=7)
    logging_level: str = Field(alias='LOGGING_LEVEL', default='INFO')
    logging_config: dict[str, Any] | None = None
    youtube_search_max_results: int = Field(alias='YOUTUBE_SEARCH_MAX_RESULTS', default=20)

    def __init__(self) -> None:
        super().__init__()
        self.logging_config = self.logging_config or {
            'disable_existing_loggers': False,
            'formatters': {
                'simple': {
                    'datefmt': '%d-%m-%Y %H:%M:%S',
                    'format': '%(asctime)s.%(msecs)03d - [%(levelname)s] - [%(name)s] - %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple'
                }
            },
            'root': {
                'handlers': [
                    'console'
                ],
                'level': self.logging_level
            },
            'version': 1
        }
