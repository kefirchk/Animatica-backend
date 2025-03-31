from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from starlette.responses import JSONResponse


class GenerateRandomVideoUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo | None

    class Response(ResponseModel):
        pass

    async def execute(self, request: Request) -> JSONResponse:
        try:
            raise NotImplemented
            return ResponseSuccess.build(self.Response())
        except Exception as exc:
            return ResponseFailure.build(exc)
