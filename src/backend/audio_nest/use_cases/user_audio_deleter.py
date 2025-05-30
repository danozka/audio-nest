import logging
from logging import Logger
from uuid import UUID

from audio_nest.services.i_user_audio_repository import IUserAudioRepository


class UserAudioDeleter:
    _log: Logger = logging.getLogger(__name__)
    _user_audio_repository: IUserAudioRepository

    def __init__(self, user_audio_repository: IUserAudioRepository) -> None:
        self._user_audio_repository = user_audio_repository

    async def delete_user_audio(self, user_audio_id: UUID) -> None:
        self._log.debug(f'Deleting user audio \'{user_audio_id}\'...')
        await self._user_audio_repository.delete_user_audio(user_audio_id)
        self._log.debug(f'User audio \'{user_audio_id}\' deleted')
