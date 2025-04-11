from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.domain.entities.enums import APIModeEnum, LogLevelEnum


class APIConfig(BaseSettings):
    BASE_URL: str = Field(..., alias="API_BASE_URL")
    FRONTEND_BASE_URL: str = Field(..., alias="FRONTEND_BASE_URL")
    MODE: APIModeEnum = Field(..., alias="API_MODE")
    LOG_LEVEL: LogLevelEnum = Field(..., alias="LOG_LEVEL")
    SESSION_SECRET_KEY: str = Field(..., alias="SESSION_SECRET_KEY")
    LOCALHOST_CLIENT_ORIGIN: str = Field(..., alias="LOCALHOST_CLIENT_ORIGIN")
    ALLOWED_ORIGINS_STR: str = Field(..., alias="ALLOWED_ORIGINS")

    model_config = SettingsConfigDict(env_file="../env/api.env")

    @property
    def allowed_origins(self) -> list[str]:
        origins = {origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")}
        if self.MODE in (APIModeEnum.LOCAL, APIModeEnum.DEV, APIModeEnum.STAGE):
            origins.add(self.LOCALHOST_CLIENT_ORIGIN)
        return sorted(origins)
