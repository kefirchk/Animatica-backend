from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthConfig(BaseSettings):
    SECRET_KEY: str = Field(..., alias="SECRET_KEY")
    ALGORITHM: str = Field(..., alias="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(..., alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(..., alias="REFRESH_TOKEN_EXPIRE_DAYS")
    TOKEN_ISSUER: str = Field(..., alias="TOKEN_ISSUER")

    model_config = SettingsConfigDict(env_file="../env/auth.env")
