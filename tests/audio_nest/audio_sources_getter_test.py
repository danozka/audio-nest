from unittest.mock import AsyncMock

import pytest

from audio_nest.domain.audio_source import AudioSource
from audio_nest.services.i_audio_sources_repository import IAudioSourcesRepository
from audio_nest.use_cases.audio_sources_getter import AudioSourcesGetter


@pytest.fixture(scope='function')
def audio_sources_repository_mock() -> AsyncMock:
    return AsyncMock(spec=IAudioSourcesRepository)


@pytest.fixture(scope='function')
def audio_sources_getter(audio_sources_repository_mock: AsyncMock) -> AudioSourcesGetter:
    return AudioSourcesGetter(audio_sources_repository_mock)


@pytest.mark.asyncio
async def test_audio_sources_are_returned(
    audio_sources_getter: AudioSourcesGetter,
    audio_sources_repository_mock: AsyncMock
) -> None:
    test_search_query: str = 'test_query'
    test_audio_sources: list[AudioSource] = [
        AudioSource(
            id='audio_source_1',
            name='Audio Source 1',
            thumbnail_url='http://test.com'
        ),
        AudioSource(
            id='audio_source_2',
            name='Audio Source 2',
            thumbnail_url=None
        )
    ]
    audio_sources_repository_mock.get_audio_sources.return_value = test_audio_sources
    result: list[AudioSource] = await audio_sources_getter.get_audio_sources(test_search_query)
    audio_sources_repository_mock.get_audio_sources.assert_awaited_once_with(test_search_query)
    assert result == test_audio_sources
