from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    logging_level: str = Field(alias='LOGGING_LEVEL', default='INFO')
    app_host: str = Field(alias='APP_HOST', default='0.0.0.0')
    app_port: int = Field(alias='APP_HOST', default=8000)
    json_web_token_secret_key: str = Field(alias='JWT_SECRET_KEY', default='my_secret_key')
    json_web_token_algorithm: str = Field(alias='JWT_ALGORITHM', default='HS256')
    json_web_token_expiration_days: int = Field(alias='JWT_ACCESS_TOKEN_EXPIRATION_DAYS', default=7)
    database_path: Path = Field(alias='DATABASE_PATH', default=Path('./data/audio-nest.db'))
    logging_config: dict[str, Any] | None = None

    def __init__(self) -> None:
        super().__init__()
        self.logging_config = {
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
