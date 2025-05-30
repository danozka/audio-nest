from uuid import UUID


class UserAudioNotFoundException(Exception):
    def __init__(self, user_audio_id: UUID) -> None:
        super().__init__(f'User audio \'{user_audio_id}\' not found')
