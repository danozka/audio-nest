from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient
from httpx import Response

from authentication.authentication_service import AuthenticationService
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.exceptions.user_already_registered_exception import UserAlreadyRegisteredException
from container import Container


REGISTER_ENDPOINT: str = '/api/auth/register'


@pytest.fixture(scope='function')
def authentication_service_mock() -> AsyncMock:
    return AsyncMock(spec=AuthenticationService)


def test_user_is_registered(
    test_container: Container,
    test_client: TestClient,
    authentication_service_mock: AsyncMock
) -> None:
    test_username: str = 'test_user'
    test_password: str = 'password123'
    with test_container.authentication_service.override(authentication_service_mock):
        response: Response = test_client.post(
            url=REGISTER_ENDPOINT,
            data={
                'username': test_username,
                'password': test_password
            }
        )
    assert response.status_code == 200
    authentication_service_mock.register_user.assert_awaited_once_with(email=test_username, password=test_password)


def test_registering_user_already_registered_returns_http_200(
    test_container: Container,
    test_client: TestClient,
    authentication_service_mock: AsyncMock
) -> None:
    test_username: str = 'test_user'
    test_password: str = 'password123'
    authentication_service_mock.register_user.side_effect = UserAlreadyRegisteredException(test_username)
    with test_container.authentication_service.override(authentication_service_mock):
        response: Response = test_client.post(
            url=REGISTER_ENDPOINT,
            data={
                'username': test_username,
                'password': test_password
            }
        )
    assert response.status_code == 200
    authentication_service_mock.register_user.assert_awaited_once_with(email=test_username, password=test_password)
