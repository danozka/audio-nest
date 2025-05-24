import logging
from logging import Logger

from authentication.domain.user import User
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.services.i_users_repository import IUsersRepository
from authentication.services.json_web_token_handler import JsonWebTokenHandler


class UserGetter:
    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository
    _json_web_token_handler: JsonWebTokenHandler

    def __init__(self, users_repository: IUsersRepository, json_web_token_handler: JsonWebTokenHandler) -> None:
        self._users_repository = users_repository
        self._json_web_token_handler = json_web_token_handler

    async def get_user_from_access_token(self, token: str) -> User:
        self._log.debug('Getting user from access token...')
        email: str | None = self._json_web_token_handler.decode_access_token(token)
        if email is None:
            raise InvalidUserCredentialsException
        user: User | None = await self._users_repository.get_user_by_email(email)
        if user is None:
            raise InvalidUserCredentialsException
        self._log.debug(f'User \'{email}\' retrieved from access token')
        return user
