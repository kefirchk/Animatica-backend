from pydantic import Field
from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    SECRET_KEY: str = Field("your-secret-key")
    ALGORITHM: str = Field("HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(30)
    TOKEN_ISSUER: str = Field("Animatica")
