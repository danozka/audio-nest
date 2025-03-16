class UserAlreadyRegisteredException(Exception):
    def __init__(self, email: str) -> None:
        super().__init__(f'User \'{email}\' already registered')
