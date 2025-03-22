import json
from typing import Optional

from fastapi import Depends, HTTPException, Request, WebSocket
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jwt import PyJWTError
from jwt.algorithms import RSAAlgorithm
from pydantic import BaseModel
from src.infrastructure.exceptions.exceptions import ExpiredTokenException
from starlette.status import HTTP_401_UNAUTHORIZED


class UserAuthInfo(BaseModel):
    sub_id: str


class JWTBearer(HTTPBearer):
    __public_keys = None

    def jwk_to_pem(self, jwk: dict):
        return RSAAlgorithm.from_jwk(json.dumps(jwk))

    def _get_credentials_from_query_token(self, ws: WebSocket) -> HTTPAuthorizationCredentials | None:
        token: str | None = ws.query_params.get("token")
        scheme, credentials = get_authorization_scheme_param(token)
        if not (token and scheme and credentials) or scheme.lower() != "bearer":
            return None
        return HTTPAuthorizationCredentials(scheme=scheme, credentials=credentials)

    async def __call__(self, request: Request = None, websocket: WebSocket = None) -> Optional[UserAuthInfo]:
        if websocket:
            credentials = self._get_credentials_from_query_token(websocket)
            if not credentials:
                return None
        else:
            credentials = await super().__call__(request)
            if not credentials:
                return None

        try:
            sub = await self._verify_token(credentials.credentials)

        except PyJWTError:
            if self.auto_error:
                raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail=f"Invalid token")
            raise ExpiredTokenException()

        return UserAuthInfo(sub_id=sub)

    async def _verify_token(self, token: str):
        response = self.openid_client.introspect(token, token_type_hint="rpt")
        if response.get("active"):
            return response.get("sub")
        raise PyJWTError()


class JWTBearerStub:
    async def __call__(self, request: Request, _: Depends = Depends()):
        return UserAuthInfo(sub_id="stub")


class JWTBearerStubWebsocket:
    async def __call__(self, websocket: WebSocket, _: Depends = Depends()):
        return UserAuthInfo(sub_id="stub")
