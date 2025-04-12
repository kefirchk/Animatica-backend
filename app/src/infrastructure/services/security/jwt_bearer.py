import jwt
from fastapi import Request, status
from fastapi.security import HTTPBearer
from src.domain.entities.auth import UserAuthInfo
from src.infrastructure.configs import AuthConfig
from src.infrastructure.exceptions.exceptions import ExpiredTokenException
from src.infrastructure.services.auth.token import TokenService


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.token_service = TokenService()
        self.config = AuthConfig()

    async def __call__(self, request: Request = None) -> UserAuthInfo | None:
        credentials = await super().__call__(request)
        if not credentials:
            return None

        try:
            payload = self.token_service.verify_token(credentials.credentials)
            return UserAuthInfo(sub_id=payload["sub"])
        except jwt.PyJWTError:
            if self.auto_error:
                raise ExpiredTokenException("Invalid or expired token", status.HTTP_401_UNAUTHORIZED)
            return None
