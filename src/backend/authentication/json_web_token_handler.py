from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import PyJWTError


class JsonWebTokenHandler:
    _secret_key: str
    _algorithm: str
    _expiration_days: int

    def __init__(self, secret_key: str, algorithm: str, expiration_days: int) -> None:
        self._secret_key = secret_key
        self._algorithm = algorithm
        self._expiration_days = expiration_days

    def create_access_token(self, subject: str) -> str:
        return jwt.encode(
            payload={
                'sub': subject,
                'exp': (datetime.now(timezone.utc) + timedelta(days=self._expiration_days))
            },
            key=self._secret_key,
            algorithm=self._algorithm
        )

    def decode_access_token(self, token: str) -> str | None:
        try:
            payload: dict[str, str | int] = jwt.decode(jwt=token, key=self._secret_key, algorithms=[self._algorithm])
            return payload.get('sub')
        except PyJWTError:
            return None
