from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.configs.auth_config import AuthConfig
from src.infrastructure.exceptions.exceptions import (
    InvalidCredentialsException,
)
from src.infrastructure.services.auth import AuthService
from src.infrastructure.services.auth.token import TokenService
from starlette.responses import JSONResponse


class UserLoginUseCase(IUseCase):
    class Request(RequestModel):
        username: str
        password: str

    class Response(ResponseModel):
        token_name: str
        refresh_token: str
        access_token: str
        access_expires_in: int
        refresh_expires_in: int

    def __init__(self) -> None:
        self.auth_service = AuthService()
        self.token_service = TokenService()
        self.auth_config = AuthConfig()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            user = await self.auth_service.authenticate_user(request.username, request.password)
            if not user:
                raise InvalidCredentialsException("Invalid username or password")

            token_data = await self.token_service.generate_tokens(user.username)

            return ResponseSuccess.build(
                self.Response(
                    token_type="Bearer",
                    access_token=token_data["access_token"],
                    refresh_token=token_data["refresh_token"],
                    access_expires_in=token_data["access_expires_in"],
                    refresh_expires_in=token_data["refresh_expires_in"],
                )
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
