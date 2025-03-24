import logging
from logging import Logger

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from api.dtos.authentication_token_dto import AuthenticationTokenDto
from authentication.exceptions.invalid_user_credentials_exception import InvalidUserCredentialsException
from authentication.exceptions.user_already_registered_exception import UserAlreadyRegisteredException
from authentication.authentication_service import AuthenticationService


log: Logger = logging.getLogger(__name__)
router: APIRouter = APIRouter(prefix='/api/auth')
oauth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='api/auth/token')


@router.post('/register')
@inject
async def register_user(
    user_data: OAuth2PasswordRequestForm = Depends(),
    authentication_service: AuthenticationService = Depends(Provide['authentication_service'])
) -> None:
    log.info(f'Registering user \'{user_data.username}\'...')
    try:
        await authentication_service.register_user(email=user_data.username, password=user_data.password)
        log.info(f'User \'{user_data.username}\' registered')
    except UserAlreadyRegisteredException as ex:
        log.warning(f'Registration failed for user \'{user_data.username}\': {ex}')
    except Exception as ex:
        log.error(f'Exception found while registering user \'{user_data.username}\': {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while registering user')


@router.post('/token')
@inject
async def log_in_for_authentication_token(
    user_data: OAuth2PasswordRequestForm = Depends(),
    authentication_service: AuthenticationService = Depends(Provide['authentication_service'])
) -> AuthenticationTokenDto:
    log.info(f'Logging user \'{user_data.username}\' in...')
    try:
        access_token: str = await authentication_service.log_in_user_for_access_token(
            email=user_data.username,
            password=user_data.password
        )
        return AuthenticationTokenDto(access_token=access_token, token_type='bearer')
    except InvalidUserCredentialsException as ex:
        log.error(f'Login failed for user \'{user_data.username}\': {ex}')
        raise HTTPException(
            status_code=401,
            detail='Could not validate user credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    except Exception as ex:
        log.error(f'Exception found while logging user \'{user_data.username}\' in: {ex}')
        raise HTTPException(status_code=500, detail='An unexpected error occurred while logging user in')
