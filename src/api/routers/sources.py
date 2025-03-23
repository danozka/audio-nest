import logging
from logging import Logger

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from adapters.audio_sources_adapter import AudioSourcesAdapter
from api.dtos.audio_source_dto import AudioSourceDto
from audio_nest.domain.audio import Audio
from audio_nest.use_cases.audio_getter import AudioGetter
from audio_nest.use_cases.audio_sources_getter import AudioSourcesGetter


log: Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix='/api/sources', tags=['sources'])


@router.get('')
@inject
async def get_audio_sources(
    search_query: str,
    audio_sources_getter: AudioSourcesGetter = Depends(Provide['audio_sources_getter'])
) -> list[AudioSourceDto]:
    log.info(f'Getting audio sources for search query \'{search_query}\'...')
    try:
        audio_sources_adapter: AudioSourcesAdapter = AudioSourcesAdapter()
        result: list[AudioSourceDto] = audio_sources_adapter.adapt_audio_sources(
            await audio_sources_getter.get_audio_sources(search_query)
        )
        log.info(f'Audio sources for search query \'{search_query}\' retrieved')
        return result
    except Exception as ex:
        log.error(f'Exception found while getting audio sources for search query \'{search_query}\': {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while getting audio sources')


@router.get('/{source_id}/audio')
@inject
async def get_audio_from_video(
    source_id: str,
    audio_getter: AudioGetter = Depends(Provide['audio_getter'])
) -> FileResponse:
    log.info(f'Getting audio from source ID \'{source_id}\'...')
    try:
        audio: Audio = await audio_getter.get_audio_from_source(source_id)
        log.info(f'Audio from source ID \'{source_id}\' retrieved')
        return FileResponse(audio.file_path)
    except Exception as ex:
        log.error(f'Exception found while getting audio from source ID \'{source_id}\': {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while getting audio')
