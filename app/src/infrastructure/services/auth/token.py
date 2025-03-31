from datetime import datetime, timedelta, timezone

import jwt
from src.domain.entities.enums import TokenType
from src.infrastructure.configs import AuthConfig


class TokenService:
    def __init__(self):
        self.auth_config = AuthConfig()

    async def generate_tokens(self, username: str) -> dict:
        """Generate access and refresh tokens"""
        access_token_expires = timedelta(minutes=self.auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_expires = timedelta(days=self.auth_config.REFRESH_TOKEN_EXPIRE_DAYS)

        access_token = self._create_token(
            data={"sub": username},  # username as unique value
            token_type=TokenType.ACCESS,
            expires_delta=access_token_expires,
        )

        refresh_token = self._create_token(
            data={"sub": username}, token_type=TokenType.REFRESH, expires_delta=refresh_token_expires
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "access_expires_in": int(access_token_expires.total_seconds()),
            "refresh_expires_in": int(refresh_token_expires.total_seconds()),
        }

    def verify_token(self, token: str) -> dict:
        """Verify JWT token and return payload"""
        return jwt.decode(
            token, self.auth_config.SECRET_KEY, algorithms=[self.auth_config.ALGORITHM], options={"verify_exp": True}
        )

    def _create_token(self, data: dict, token_type: TokenType, expires_delta: timedelta | None = None) -> str:
        """Base token creation method"""
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + (
            expires_delta if expires_delta else timedelta(minutes=self.auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        to_encode.update({"exp": expire, "type": token_type, "iss": self.auth_config.TOKEN_ISSUER})

        return jwt.encode(payload=to_encode, key=self.auth_config.SECRET_KEY, algorithm=self.auth_config.ALGORITHM)
