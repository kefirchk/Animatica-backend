from typing import Annotated

from fastapi import Depends
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseSuccess,
    TokensResponseModel,
)
from src.domain.interfaces import IDBRepository, IUseCase
from src.infrastructure.exceptions.exceptions import NoSuchItem
from src.infrastructure.repositories import DBRepository
from starlette.responses import JSONResponse


class ResetPasswordUseCase(IUseCase):
    class Request(RequestModel):
        token: str
        password: str

    class Response(TokensResponseModel):
        pass

    def __init__(
        self,
        db_repository: Annotated[IDBRepository, Depends(DBRepository)],
    ) -> None:
        self.db_repository = db_repository

    async def execute(self, request: Request) -> JSONResponse:
        try:
            payload = self.token_handler.decode_token(request.token)
            async with self.db_repository as db_repository:
                user = await db_repository.get_user_by_email(payload["email"])

            if not user:
                raise NoSuchItem("User with this email does not exist")

            await self.keycloak_repository.set_password(user.sub, request.password)
            tokens = await self.keycloak_repository.login(payload["email"], request.password)

            return ResponseSuccess.build(
                self.Response(
                    refresh_token=tokens["refresh_token"],
                    access_token=tokens["access_token"],
                    expires_in=tokens["expires_in"],
                    refresh_expires_in=tokens["refresh_expires_in"],
                )
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
