from abc import ABC, abstractmethod

from auth.domain.user import User


class IUsersRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, user: User) -> None:
        pass
