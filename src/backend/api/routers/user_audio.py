import logging
from logging import Logger
from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from api.dtos.user_audio_dto import UserAudioDto
from api.routers.authentication import oauth2_scheme
from audio_nest.domain.user_audio import UserAudio
from audio_nest.exceptions.user_audio_not_found_exception import UserAudioNotFoundException
from audio_nest.use_cases.user_audio_deleter import UserAudioDeleter
from audio_nest.use_cases.user_audio_getter import UserAudioGetter
from audio_nest.use_cases.user_audio_list_getter import UserAudioListGetter
from authentication.domain.user import User
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.use_cases.user_getter import UserGetter


log: Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix='/api/user-audio')


@router.get('')
@inject
async def get_user_audio_list(
    token: str = Depends(oauth2_scheme),
    user_audio_list_getter: UserAudioListGetter = Depends(Provide['user_audio_list_getter']),
    user_getter: UserGetter = Depends(Provide['user_getter'])
) -> list[UserAudioDto]:
    log.info(f'Getting user audio list...')
    try:
        user: User = await user_getter.get_user_from_access_token(token)
        user_audio_list: list[UserAudioDto] = [
            UserAudioDto.model_validate(user_audio.__dict__)
            for user_audio in await user_audio_list_getter.get_user_audio_list(user.id)
        ]
        log.info(f'User \'{user.id}\' audio list retrieved')
        return user_audio_list
    except InvalidUserCredentialsException as ex:
        log.error(f'Authentication failed: {ex}')
        raise HTTPException(
            status_code=401,
            detail='Could not validate user credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except Exception as ex:
        log.error(f'Exception found while getting user audio list: {ex.__class__.__name__} - {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while getting user audio list')


@router.get(path='/{user_audio_id}')
@inject
async def get_user_audio(
    user_audio_id: UUID,
    token: str = Depends(oauth2_scheme),
    user_audio_getter: UserAudioGetter = Depends(Provide['user_audio_getter']),
    user_getter: UserGetter = Depends(Provide['user_getter'])
) -> FileResponse:
    log.info(f'Getting user audio \'{user_audio_id}\'...')
    try:
        await user_getter.get_user_from_access_token(token)
        user_audio: UserAudio = await user_audio_getter.get_user_audio(user_audio_id)
        log.info(f'User audio \'{user_audio_id}\' retrieved')
        return FileResponse(user_audio.file_path)
    except InvalidUserCredentialsException as ex:
        log.error(f'Authentication failed: {ex}')
        raise HTTPException(
            status_code=401,
            detail='Could not validate user credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except UserAudioNotFoundException as ex:
        log.error(f'Failed to get user audio: {ex}')
        raise HTTPException(status_code=404, detail='User audio not found')
    except Exception as ex:
        log.error(f'Exception found while getting user audio: {ex.__class__.__name__} - {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while getting user audio')


@router.delete(path='/{user_audio_id}')
@inject
async def delete_user_audio(
    user_audio_id: UUID,
    token: str = Depends(oauth2_scheme),
    user_audio_deleter: UserAudioDeleter = Depends(Provide['user_audio_deleter']),
    user_getter: UserGetter = Depends(Provide['user_getter'])
) -> None:
    log.info(f'Deleting user audio \'{user_audio_id}\'...')
    try:
        await user_getter.get_user_from_access_token(token)
        await user_audio_deleter.delete_user_audio(user_audio_id)
        log.info(f'User audio \'{user_audio_id}\' deleted')
    except InvalidUserCredentialsException as ex:
        log.error(f'Authentication failed: {ex}')
        raise HTTPException(
            status_code=401,
            detail='Could not validate user credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except Exception as ex:
        log.error(f'Exception found while deleting user audio: {ex.__class__.__name__} - {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while deleting user audio')
