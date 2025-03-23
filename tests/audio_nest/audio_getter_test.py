from pathlib import Path
from unittest.mock import AsyncMock

import pytest

from audio_nest.domain.audio import Audio
from audio_nest.domain.audio_codec import AudioCodec
from audio_nest.services.i_audio_repository import IAudioRepository
from audio_nest.use_cases.audio_getter import AudioGetter


@pytest.fixture(scope='function')
def audio_repository_mock() -> AsyncMock:
    return AsyncMock(spec=IAudioRepository)


@pytest.fixture(scope='function')
def audio_getter(audio_repository_mock: AsyncMock) -> AudioGetter:
    return AudioGetter(audio_repository_mock)


@pytest.mark.asyncio
async def test_audio_is_returned(audio_getter: AudioGetter, audio_repository_mock: AsyncMock) -> None:
    test_source_id: str = 'test_source_id'
    test_audio: Audio = Audio(
        source_id=test_source_id, 
        file_path=Path('./test_audio.ogg'),
        bit_rate_kbps=320,
        codec=AudioCodec.vorbis
    )
    audio_repository_mock.get_audio_from_source.return_value = test_audio
    result: Audio = await audio_getter.get_audio_from_source(test_source_id)
    audio_repository_mock.get_audio_from_source.assert_awaited_once_with(test_source_id)
    assert result == test_audio
