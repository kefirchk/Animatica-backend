from typing import Annotated

from fastapi import Depends
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IDBRepository, IUseCase
from src.infrastructure.exceptions.exceptions import NoSuchItem
from src.infrastructure.repositories import DBRepository
from starlette.responses import JSONResponse


class ForgotPasswordUseCase(IUseCase):
    class Request(RequestModel):
        email: str

    class Response(ResponseModel):
        pass

    def __init__(
        self,
        db_repository: Annotated[IDBRepository, Depends(DBRepository)],
    ) -> None:
        self.db_repository = db_repository

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.db_repository as db_repository:
                user = await db_repository.get_user_by_email(request.email)

            if not user:
                raise NoSuchItem("User with this email does not exist")

            token = self.token_handler.generate_token(request.email)

            await self.email_sender.send_password_reset_email(request.email, token, user.name)
            return ResponseSuccess.build(self.Response())
        except Exception as exc:
            return ResponseFailure.build(exc)
