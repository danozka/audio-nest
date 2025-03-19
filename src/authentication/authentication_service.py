import logging
from logging import Logger

from passlib.context import CryptContext

from audio_nest.domain.user import User
from audio_nest.services.i_users_repository import IUsersRepository
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.exceptions.user_already_registered_exception import UserAlreadyRegisteredException
from authentication.json_web_token_handler import JsonWebTokenHandler


class AuthenticationService:
    _log: Logger = logging.getLogger(__name__)
    _json_web_token_handler: JsonWebTokenHandler
    _users_repository: IUsersRepository
    _password_context: CryptContext

    def __init__(
        self,
        json_web_token_handler: JsonWebTokenHandler,
        users_repository: IUsersRepository,
        password_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')
    ) -> None:
        self._json_web_token_handler = json_web_token_handler
        self._users_repository = users_repository
        self._password_context = password_context

    async def register_user(self, email: str, password: str) -> None:
        self._log.debug(f'Registering user \'{email}\'...')
        if await self._users_repository.get_user_by_email(email):
            raise UserAlreadyRegisteredException(email)
        user: User = User(email=email, hashed_password=self._password_context.hash(password))
        await self._users_repository.create_user(user)
        self._log.debug(f'User \'{email}\' registered')

    async def log_in_user_for_access_token(self, email: str, password: str) -> str:
        self._log.debug(f'Logging user \'{email}\' in for access token...')
        user: User | None = await self._users_repository.get_user_by_email(email)
        if not user or not self._password_context.verify(secret=password, hash=user.hashed_password):
            raise InvalidUserCredentialsException
        access_token: str = self._json_web_token_handler.create_access_token(email)
        self._log.debug(f'User \'{email}\' logged in with access token \'{access_token}\'')
        return access_token

    async def get_user_from_access_token(self, token: str) -> User:
        self._log.debug(f'Getting user from access token \'{token}\'...')
        email: str | None = self._json_web_token_handler.decode_access_token(token)
        if email is None:
            raise InvalidUserCredentialsException
        user: User | None = await self._users_repository.get_user_by_email(email)
        if user is None:
            raise InvalidUserCredentialsException
        self._log.debug(f'User \'{email}\' retrieved from access token \'{token}\'')
        return user
