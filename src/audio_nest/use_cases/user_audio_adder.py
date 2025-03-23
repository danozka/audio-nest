import logging
from logging import Logger

from audio_nest.services.i_user_audio_repository import IUserAudioRepository
from audio_nest.domain.user_audio import UserAudio
from audio_nest.exceptions.user_audio_already_added_exception import UserAudioAlreadyAddedException


class UserAudioAdder:
    _log: Logger = logging.getLogger(__name__)
    _user_audio_repository: IUserAudioRepository

    def __init__(self, user_audio_repository: IUserAudioRepository) -> None:
        self._user_audio_repository = user_audio_repository

    async def add_user_audio(self, user_audio: UserAudio) -> None:
        self._log.debug(f'Adding {user_audio}...')
        if await self._user_audio_repository.get_user_audio_from_source(user_audio.source_id):
            raise UserAudioAlreadyAddedException(user_audio)
        await self._user_audio_repository.add_user_audio(user_audio)
        self._log.debug(f'{user_audio} added')
