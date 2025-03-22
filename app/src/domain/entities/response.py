from pydantic import BaseModel
from src.infrastructure.exceptions.handlers import handle_exception
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK


class ResponseModel(BaseModel):
    pass


class TokensResponseModel(ResponseModel):
    refresh_token: str
    access_token: str
    expires_in: int
    refresh_expires_in: int


class ResponseFailure:
    def __init__(self, err_msg: str, status_code: int) -> None:
        self.err_msg = err_msg
        self.status = status_code

    @classmethod
    def build(cls, exc: Exception) -> JSONResponse:
        return JSONResponse(*handle_exception(exc))


class ResponseSuccess:
    def __init__(self, payload: ResponseModel, status: int) -> None:
        self.payload = payload
        self.status = status

    @classmethod
    def build(cls, payload: ResponseModel | list[ResponseModel], status: int = HTTP_200_OK, **kwargs) -> JSONResponse:
        if isinstance(payload, list):
            content = [item.model_dump(**kwargs) for item in payload]
        else:
            content = payload.model_dump(**kwargs)

        return JSONResponse(content=content, status_code=status)
