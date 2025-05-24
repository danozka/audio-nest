import logging
from logging import Logger

from authentication.domain.user import User
from authentication.exceptions.user_already_registered_exception import UserAlreadyRegisteredException
from authentication.services.i_users_repository import IUsersRepository
from authentication.services.password_hasher import PasswordHasher


class UserRegistrationHandler:
    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository
    _password_hasher: PasswordHasher

    def __init__(self, users_repository: IUsersRepository, password_hasher: PasswordHasher = PasswordHasher()) -> None:
        self._users_repository = users_repository
        self._password_hasher = password_hasher

    async def register_user(self, email: str, password: str) -> None:
        self._log.debug(f'Registering user with email \'{email}\'...')
        if await self._users_repository.get_user_by_email(email):
            raise UserAlreadyRegisteredException(email)
        user: User = User(email=email, hashed_password=self._password_hasher.hash_password(password))
        await self._users_repository.create_user(user)
        self._log.debug(f'User with email \'{email}\' registered')
