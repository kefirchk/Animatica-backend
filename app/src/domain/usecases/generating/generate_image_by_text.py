from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.services.auth import UserAuthInfo
from starlette.responses import JSONResponse


class GenerateImageByTextUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo | None
        text: str

    class Response(ResponseModel):
        pass

    async def execute(self, request: Request) -> JSONResponse:
        try:
            return ResponseSuccess.build(self.Response())
        except Exception as exc:
            return ResponseFailure.build(exc)
