from unittest.mock import AsyncMock, Mock

import pytest
from passlib.context import CryptContext

from authentication.domain.user import User
from audio_nest.services.i_users_repository import IUsersRepository
from authentication.authentication_service import AuthenticationService
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.exceptions.user_already_registered_exception import UserAlreadyRegisteredException
from authentication.services.json_web_token_handler import JsonWebTokenHandler


@pytest.fixture(scope='function')
def json_web_token_handler_mock() -> Mock:
    return Mock(spec=JsonWebTokenHandler)


@pytest.fixture(scope='function')
def users_repository_mock() -> AsyncMock:
    return AsyncMock(spec=IUsersRepository)


@pytest.fixture(scope='function')
def password_context_mock() -> Mock:
    return Mock(spec=CryptContext)


@pytest.fixture(scope='function')
def authentication_service(
    json_web_token_handler_mock: Mock,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock
) -> AuthenticationService:
    return AuthenticationService(
        json_web_token_handler=json_web_token_handler_mock,
        users_repository=users_repository_mock,
        password_context=password_context_mock
    )


@pytest.mark.asyncio
async def test_user_is_registered(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_password: str = 'password123'
    users_repository_mock.get_user_by_email.return_value = None
    password_context_mock.hash.return_value = 'hashed_password'
    await authentication_service.register_user(email=test_email, password=test_password)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    password_context_mock.hash.assert_called_once_with(test_password)
    users_repository_mock.create_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_registering_user_already_registered_raises_exception(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_password: str = 'password123'
    users_repository_mock.get_user_by_email.return_value = User(email=test_email, hashed_password='hashed_password')
    with pytest.raises(UserAlreadyRegisteredException):
        await authentication_service.register_user(email=test_email, password=test_password)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    password_context_mock.hash.assert_not_called()
    users_repository_mock.create_user.assert_not_awaited()


@pytest.mark.asyncio
async def test_access_token_is_returned_after_logging_in_user(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock,
    json_web_token_handler_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_password: str = 'password123'
    test_hashed_password: str = 'hashed_password'
    test_user: User = User(email=test_email, hashed_password=test_hashed_password)
    test_access_token: str = 'access_token'
    users_repository_mock.get_user_by_email.return_value = test_user
    password_context_mock.verify.return_value = True
    json_web_token_handler_mock.create_access_token.return_value = test_access_token
    result: str = await authentication_service.log_in_user_for_access_token(email=test_email, password=test_password)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    password_context_mock.verify.assert_called_once_with(secret=test_password, hash=test_hashed_password)
    json_web_token_handler_mock.create_access_token.assert_called_once_with(test_email)
    assert result == test_access_token


@pytest.mark.asyncio
async def test_logging_in_user_with_invalid_email_raises_exception(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock,
    json_web_token_handler_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    users_repository_mock.get_user_by_email.return_value = None
    with pytest.raises(InvalidUserCredentialsException):
        await authentication_service.log_in_user_for_access_token(email=test_email, password='password123')
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    password_context_mock.verify.assert_not_called()
    json_web_token_handler_mock.create_access_token.assert_not_called()


@pytest.mark.asyncio
async def test_logging_in_user_with_invalid_password_raises_exception(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    password_context_mock: Mock,
    json_web_token_handler_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_password: str = 'password123'
    test_hashed_password: str = 'hashed_password'
    test_user: User = User(email=test_email, hashed_password=test_hashed_password)
    users_repository_mock.get_user_by_email.return_value = test_user
    password_context_mock.verify.return_value = False
    with pytest.raises(InvalidUserCredentialsException):
        await authentication_service.log_in_user_for_access_token(email=test_email, password=test_password)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    password_context_mock.verify.assert_called_once_with(secret=test_password, hash=test_hashed_password)
    json_web_token_handler_mock.create_access_token.assert_not_called()


@pytest.mark.asyncio
async def test_user_is_returned_from_access_token(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    json_web_token_handler_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_user: User = User(email=test_email, hashed_password='hashed_password')
    test_access_token: str = 'access_token'
    json_web_token_handler_mock.decode_access_token.return_value = test_email
    users_repository_mock.get_user_by_email.return_value = test_user
    result: User = await authentication_service.get_user_from_access_token(test_access_token)
    json_web_token_handler_mock.decode_access_token.assert_called_once_with(test_access_token)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
    assert result == test_user


@pytest.mark.asyncio
async def test_getting_user_from_invalid_access_token_raises_exception(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    json_web_token_handler_mock: Mock
) -> None:
    test_access_token: str = 'access_token'
    json_web_token_handler_mock.decode_access_token.return_value = None
    with pytest.raises(InvalidUserCredentialsException):
        await authentication_service.get_user_from_access_token(test_access_token)
    json_web_token_handler_mock.decode_access_token.assert_called_once_with(test_access_token)
    users_repository_mock.get_user_by_email.assert_not_awaited()


@pytest.mark.asyncio
async def test_getting_unknown_user_from_access_token_raises_exception(
    authentication_service: AuthenticationService,
    users_repository_mock: AsyncMock,
    json_web_token_handler_mock: Mock
) -> None:
    test_email: str = 'test@example.com'
    test_access_token: str = 'access_token'
    json_web_token_handler_mock.decode_access_token.return_value = test_email
    users_repository_mock.get_user_by_email.return_value = None
    with pytest.raises(InvalidUserCredentialsException):
        await authentication_service.get_user_from_access_token(test_access_token)
    json_web_token_handler_mock.decode_access_token.assert_called_once_with(test_access_token)
    users_repository_mock.get_user_by_email.assert_awaited_once_with(test_email)
