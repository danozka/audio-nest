import logging
from logging import Logger
from uuid import UUID

from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.domain.user_audio import UserAudio


class UserAudioGetter:
    _log: Logger = logging.getLogger(__name__)
    _user_audio_repository: IUserAudioRepository

    def __init__(self, user_audio_repository: IUserAudioRepository) -> None:
        self._user_audio_repository = user_audio_repository

    async def get_user_audio_list(self, user_id: UUID) -> list[UserAudio]:
        self._log.debug(f'Getting user \'{user_id}\' audio list...')
        user_audio_list: list[UserAudio] = await self._user_audio_repository.get_user_audio_list(user_id)
        self._log.debug(f'User \'{user_id}\' audio list retrieved')
        return user_audio_list
