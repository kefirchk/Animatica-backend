from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.exceptions.exceptions import UserAlreadyExistsException
from src.infrastructure.repositories.user_repository import UserRepository
from starlette import status
from starlette.responses import JSONResponse


class UserSignUpUseCase(IUseCase):
    class Request(RequestModel):
        password: str
        username: str

    class Response(ResponseModel):
        pass

    def __init__(self) -> None:
        self.user_repository = UserRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.user_repository as repository:
                if await repository.get_user_by_username(request.username):
                    raise UserAlreadyExistsException(f"Username '{request.username}' already exists")

                await repository.create_user(username=request.username, password=request.password)

            return ResponseSuccess.build(self.Response(), status=status.HTTP_201_CREATED)

        except Exception as exc:
            return ResponseFailure.build(exc)
