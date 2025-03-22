from typing import Annotated

from fastapi import Depends
from src.domain.entities.request import RequestModel
from src.domain.entities.response import ResponseFailure, ResponseModel
from src.domain.interfaces import IDBRepository, IUseCase
from src.infrastructure.exceptions.exceptions import UserExistsException
from src.infrastructure.repositories import DBRepository
from starlette.responses import JSONResponse


class UserSignUpUseCase(IUseCase):
    class Request(RequestModel):
        email: str
        password: str
        name: str

    class Response(ResponseModel):
        access_token: str
        refresh_token: str

    def __init__(
        self,
        db_repository: Annotated[IDBRepository, Depends(DBRepository)],
    ) -> None:
        self.db_repository = db_repository

    async def execute(self, request: Request) -> JSONResponse:
        try:
            await self.email_sender.check_email_verified([request.email])

            async with self.db_repository:
                if await self.db_repository.get_user_by_email(request.email):
                    raise UserExistsException()

                sub = await self.repository.sign_up(
                    request.email,
                    request.password,
                    request.name,
                )

                await self.db_repository.create_user(
                    sub,
                    request.name,
                    request.email,
                    request.password,
                )

        except Exception as exc:
            return ResponseFailure.build(exc)
