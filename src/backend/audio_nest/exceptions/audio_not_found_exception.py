class AudioNotFoundException(Exception):
    def __init__(self, source_id: str) -> None:
        super().__init__(f'Audio from source \'{source_id}\' not found')
