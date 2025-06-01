class InvalidUserCredentialsException(Exception):
    def __init__(self) -> None:
        super().__init__('Could not validate user credentials')
