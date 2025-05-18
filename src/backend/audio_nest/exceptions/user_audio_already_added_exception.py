from audio_nest.domain.user_audio import UserAudio


class UserAudioAlreadyAddedException(Exception):
    def __init__(self, user_audio: UserAudio) -> None:
        super().__init__(
            f'Audio from source \'{user_audio.source_id}\' already added for user \'{user_audio.user_id}\''
        )
