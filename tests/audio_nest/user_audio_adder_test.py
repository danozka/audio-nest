from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.domain.user_audio import UserAudio
from audio_nest.exceptions.user_audio_already_added_exception import UserAudioAlreadyAddedException
from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.use_cases.user_audio_adder import UserAudioAdder


@pytest.fixture(scope='function')
def user_audio_repository_mock() -> AsyncMock:
    return AsyncMock(spec=IUserAudioRepository)


@pytest.fixture(scope='function')
def user_audio_adder(user_audio_repository_mock: AsyncMock) -> UserAudioAdder:
    return UserAudioAdder(user_audio_repository_mock)


@pytest.mark.asyncio
async def test_user_audio_is_added(user_audio_adder: UserAudioAdder, user_audio_repository_mock: AsyncMock) -> None:
    test_user_audio: UserAudio = UserAudio(
        source_id='test_source_id',
        file_path=Path('./test_audio.ogg'),
        bit_rate_kbps=320,
        codec=AudioCodec.vorbis,
        id=uuid4(),
        user_id=uuid4(),
        title='Test title',
        artist='Test artist'
    )
    user_audio_repository_mock.get_user_audio_from_source.return_value = None
    await user_audio_adder.add_user_audio(test_user_audio)
    user_audio_repository_mock.get_user_audio_from_source.assert_awaited_once_with(test_user_audio.source_id)
    user_audio_repository_mock.add_user_audio.assert_awaited_once_with(test_user_audio)


@pytest.mark.asyncio
async def test_adding_user_audio_from_existing_source_raises_exception(
    user_audio_adder: UserAudioAdder,
    user_audio_repository_mock: AsyncMock
) -> None:
    test_user_audio: UserAudio = UserAudio(
        source_id='test_source_id',
        file_path=Path('./test_audio.ogg'),
        bit_rate_kbps=320,
        codec=AudioCodec.vorbis,
        id=uuid4(),
        user_id=uuid4(),
        title='Test title',
        artist='Test artist'
    )
    user_audio_repository_mock.get_user_audio_from_source.return_value = test_user_audio
    with pytest.raises(UserAudioAlreadyAddedException):
        await user_audio_adder.add_user_audio(test_user_audio)
    user_audio_repository_mock.get_user_audio_from_source.assert_awaited_once_with(test_user_audio.source_id)
    user_audio_repository_mock.add_user_audio.assert_not_awaited()
