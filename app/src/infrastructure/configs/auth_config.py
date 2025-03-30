from pydantic import Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    TOKEN_ISSUER: str = Field("Animatica")
