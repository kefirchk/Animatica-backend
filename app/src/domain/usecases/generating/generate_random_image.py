from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from starlette.responses import JSONResponse


class GenerateRandomImageUseCase(IUseCase):
    class Request(RequestModel):
        pass

    class Response(ResponseModel):
        pass

    async def execute(self, request: Request) -> JSONResponse:
        try:
            return ResponseSuccess.build(self.Response())
        except Exception as exc:
            return ResponseFailure.build(exc)
