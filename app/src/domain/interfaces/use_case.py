from abc import ABC, abstractmethod

from src.domain.entities.response import ResponseFailure, ResponseSuccess


class IUseCase(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> ResponseSuccess | ResponseFailure:
        pass
