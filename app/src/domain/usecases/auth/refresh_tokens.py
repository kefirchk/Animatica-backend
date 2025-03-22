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


class RefreshTokensUseCase(IUseCase):
    class Request(RequestModel):
        refresh_token: str

    class Response(TokensResponseModel):
        pass

    def __init__(self, repository: Annotated[IDBRepository, Depends(DBRepository)]) -> None:
        self.repository = repository

    async def execute(self, request: Request) -> JSONResponse:
        try:
            tokens = await self.repository.refresh_token(request.refresh_token)

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
