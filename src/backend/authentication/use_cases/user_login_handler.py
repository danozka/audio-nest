import logging
from logging import Logger

from authentication.domain.user import User
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.services.i_users_repository import IUsersRepository
from authentication.services.json_web_token_handler import JsonWebTokenHandler
from authentication.services.password_hasher import PasswordHasher


class UserLoginHandler:
    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository
    _json_web_token_handler: JsonWebTokenHandler
    _password_hasher: PasswordHasher

    def __init__(
        self,
        users_repository: IUsersRepository,
        json_web_token_handler: JsonWebTokenHandler,
        password_hasher: PasswordHasher = PasswordHasher()
    ) -> None:
        self._users_repository = users_repository
        self._json_web_token_handler = json_web_token_handler
        self._password_hasher = password_hasher

    async def log_user_in(self, email: str, password: str) -> str:
        self._log.debug(f'Logging user with email \'{email}\' in...')
        user: User | None = await self._users_repository.get_user_by_email(email)
        if not user or not self._password_hasher.verify_password(
            password=password,
            hashed_password=user.hashed_password
        ):
            raise InvalidUserCredentialsException
        access_token: str = self._json_web_token_handler.create_access_token(email)
        self._log.debug(f'User with email \'{email}\' logged in')
        return access_token
