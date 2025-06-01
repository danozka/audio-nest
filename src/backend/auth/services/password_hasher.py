import logging
from logging import Logger

from passlib.context import CryptContext


class PasswordHasher:
    _log: Logger = logging.getLogger(__name__)
    _password_context: CryptContext

    def __init__(self, password_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')) -> None:
        self._password_context = password_context

    def hash_password(self, password: str) -> str:
        self._log.debug('Hashing password...')
        hashed_password: str = self._password_context.hash(password)
        self._log.debug('Password hashed successfully')
        return hashed_password

    def verify_password(self, password: str, hashed_password: str) -> bool:
        self._log.debug('Verifying password against hashed password...')
        result: bool = self._password_context.verify(secret=password, hash=hashed_password)
        self._log.debug(f'Password verification result: {result}')
        return result
