from abc import ABC, abstractmethod

from audio_nest.domain.user import User


class IUsersRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, user: User) -> None:
        raise NotImplementedError
