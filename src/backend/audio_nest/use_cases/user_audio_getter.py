import logging
from logging import Logger
from uuid import UUID

from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.domain.user_audio import UserAudio
from audio_nest.exceptions.user_audio_not_found_exception import UserAudioNotFoundException


class UserAudioGetter:
    _log: Logger = logging.getLogger(__name__)
    _user_audio_repository: IUserAudioRepository

    def __init__(self, user_audio_repository: IUserAudioRepository) -> None:
        self._user_audio_repository = user_audio_repository

    async def get_user_audio(self, user_audio_id: UUID) -> UserAudio:
        self._log.debug(f'Getting user audio \'{user_audio_id}\'...')
        user_audio: UserAudio | None = await self._user_audio_repository.get_user_audio(user_audio_id)
        if not user_audio:
            raise UserAudioNotFoundException(user_audio_id)
        self._log.debug(f'User audio \'{user_audio_id}\' retrieved')
        return user_audio
