from unittest.mock import AsyncMock

import pytest

from audio_nest.services.i_audio_repository import IAudioRepository
from audio_nest.services.i_audio_sources_repository import IAudioSourcesRepository
from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.services.i_users_repository import IUsersRepository
from container import Container


@pytest.fixture(scope='session', autouse=True)
def test_container() -> Container:
    container: Container = Container()
    container.audio_repository.override(AsyncMock(spec=IAudioRepository))
    container.audio_sources_repository.override(AsyncMock(spec=IAudioSourcesRepository))
    container.user_audio_repository.override(AsyncMock(spec=IUserAudioRepository))
    container.users_repository.override(AsyncMock(spec=IUsersRepository))
    container.logging.init()
    return container
