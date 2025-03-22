from abc import ABC, abstractmethod

from src.infrastructure.models import User


class IDBRepository(ABC):
    @abstractmethod
    async def create_user(self, sub: str, name: str, email: str, password: str) -> None:
        pass

    @abstractmethod
    async def get_user(self, user_name) -> User:
        pass

    @abstractmethod
    async def get_user_by_sub(self, sub: str) -> User:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: str) -> User:
        pass
