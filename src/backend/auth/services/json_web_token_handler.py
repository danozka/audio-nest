import logging
from datetime import datetime, timedelta, timezone
from logging import Logger

import jwt
from jwt.exceptions import PyJWTError


class JsonWebTokenHandler:
    _log: Logger = logging.getLogger(__name__)
    _secret_key: str
    _algorithm: str
    _expiration_days: int

    def __init__(self, secret_key: str, algorithm: str, expiration_days: int) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expiration_days = expiration_days

    def create_access_token(self, subject: str) -> str:
        self._log.debug(f'Creating access token for subject \'{subject}\'...')
        access_token: str = jwt.encode(
            payload={
                'sub': subject,
                'exp': (datetime.now(timezone.utc) + timedelta(days=self._expiration_days))
            },
            key=self._secret_key,
            algorithm=self._algorithm
        )
        self._log.debug(f'Access token for subject \'{subject}\' created')
        return access_token

    def decode_access_token(self, token: str) -> str | None:
        self._log.debug('Decoding access token...')
        try:
            payload: dict[str, str | int] = jwt.decode(jwt=token, key=self._secret_key, algorithms=[self._algorithm])
            subject: str | None = payload.get('sub')
            self._log.debug(f'Access token decoded with subject \'{subject}\'')
            return subject
        except PyJWTError:
            self._log.debug('Access token decoding failed')
            return None
