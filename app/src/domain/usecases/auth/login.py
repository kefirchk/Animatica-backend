from typing import Annotated

from fastapi import Depends
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseSuccess,
    TokensResponseModel,
)
from src.domain.interfaces import IDBRepository, IUseCase
from src.infrastructure.repositories import DBRepository
from starlette.responses import JSONResponse


class UserLoginUseCase(IUseCase):
    class Request(RequestModel):
        username: str
        password: str

    class Response(TokensResponseModel):
        pass

    def __init__(self, repository: Annotated[IDBRepository, Depends(DBRepository)]) -> None:
        self.repository = repository

    async def execute(self, request: Request) -> JSONResponse:
        try:
            response = await self.repository.login(request.username, request.password)
            return ResponseSuccess.build(
                self.Response(
                    refresh_token=response["refresh_token"],
                    access_token=response["access_token"],
                    expires_in=response["expires_in"],
                    refresh_expires_in=response["refresh_expires_in"],
                ),
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
