from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app import App
from container import Container


@pytest.fixture(scope='session')
def test_client(test_container: Container) -> Generator[TestClient, None, None]:
    with TestClient(app=App(test_container), raise_server_exceptions=False) as test_client:
        yield test_client
