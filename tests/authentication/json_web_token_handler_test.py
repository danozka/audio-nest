import pytest

from authentication.services.json_web_token_handler import JsonWebTokenHandler


@pytest.fixture(scope='function')
def json_web_token_handler() -> JsonWebTokenHandler:
    return JsonWebTokenHandler(secret_key='test_secret_key', algorithm='HS256', expiration_days=1)


def test_access_token_is_created(json_web_token_handler: JsonWebTokenHandler) -> None:
    access_token: str = json_web_token_handler.create_access_token('test_user')
    assert isinstance(access_token, str)
    assert len(access_token) > 0


def test_access_token_is_decoded(json_web_token_handler: JsonWebTokenHandler) -> None:
    test_subject: str = 'test_user'
    access_token: str = json_web_token_handler.create_access_token('test_user')
    result: str = json_web_token_handler.decode_access_token(access_token)
    assert result == test_subject


def test_decoding_invalid_access_token_returns_none(json_web_token_handler: JsonWebTokenHandler) -> None:
    result: str | None = json_web_token_handler.decode_access_token('invalid_token')
    assert result is None
