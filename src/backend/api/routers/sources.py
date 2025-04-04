import logging
from logging import Logger

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from adapters.audio_sources_adapter import AudioSourcesAdapter
from api.dtos.audio_source_dto import AudioSourceDto
from api.dtos.user_audio_dto import UserAudioDto
from api.routers.authentication import oauth2_scheme
from audio_nest.domain.audio import Audio
from audio_nest.domain.user import User
from audio_nest.domain.user_audio import UserAudio
from audio_nest.exceptions.user_audio_already_added_exception import UserAudioAlreadyAddedException
from audio_nest.use_cases.audio_getter import AudioGetter
from audio_nest.use_cases.audio_sources_getter import AudioSourcesGetter
from audio_nest.use_cases.user_audio_adder import UserAudioAdder
from authentication.authentication_service import AuthenticationService
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException


log: Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix='/api/sources')


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
async def get_audio_from_source(
    source_id: str,
    audio_getter: AudioGetter = Depends(Provide['audio_getter'])
) -> FileResponse:
    log.info(f'Getting audio from source \'{source_id}\'...')
    try:
        audio: Audio = await audio_getter.get_audio_from_source(source_id)
        log.info(f'Audio from source \'{source_id}\' retrieved')
        return FileResponse(audio.file_path)
    except Exception as ex:
        log.error(f'Exception found while getting audio from source \'{source_id}\': {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while getting audio from source')


@router.put('/{source_id}/audio')
@inject
async def add_user_audio_from_source(
    source_id: str,
    user_audio_dto: UserAudioDto,
    token: str = Depends(oauth2_scheme),
    authentication_service: AuthenticationService = Depends(Provide['authentication_service']),
    audio_getter: AudioGetter = Depends(Provide['audio_getter']),
    user_audio_adder: UserAudioAdder = Depends(Provide['user_audio_adder'])
) -> None:
    log.info(f'Adding {user_audio_dto} from source \'{source_id}\'...')
    try:
        user: User = await authentication_service.get_user_from_access_token(token)
        audio: Audio = await audio_getter.get_audio_from_source(source_id)
        user_audio: UserAudio = UserAudio(
            id=user_audio_dto.id,
            user_id=user.id,
            title=user_audio_dto.title,
            artist=user_audio_dto.artist,
            source_id=audio.source_id,
            file_path=audio.file_path,
            bit_rate_kbps=audio.bit_rate_kbps,
            codec=audio.codec
        )
        await user_audio_adder.add_user_audio(user_audio)
        log.info(f'{user_audio_dto} from source \'{source_id}\' added')
    except InvalidUserCredentialsException as ex:
        log.error(f'Authentication failed: {ex}')
        raise HTTPException(
            status_code=401,
            detail='Could not validate user credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except UserAudioAlreadyAddedException as ex:
        log.error(f'Failed to add user audio: {ex}')
        raise HTTPException(status_code=409, detail='Audio already added for user')
    except Exception as ex:
        log.error(f'Exception found while adding {user_audio_dto} from source \'{source_id}\': {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while adding user audio')
