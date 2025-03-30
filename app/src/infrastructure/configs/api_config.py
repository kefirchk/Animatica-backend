from urllib.parse import urljoin

from pydantic import Field
from pydantic_settings import BaseSettings
from src.domain.entities.enums import APIModeEnum, LogLevelEnum


class APIConfig(BaseSettings):
    URL: str = Field("http://localhost:8080", alias="API_URL")
    MODE: APIModeEnum = Field(APIModeEnum.LOCAL, alias="API_MODE")
    LOG_LEVEL: LogLevelEnum = Field(LogLevelEnum.INFO, alias="LOG_LEVEL")
    allowed_origins_str: str = Field("localhost", alias="ALLOWED_ORIGINS")
    session_secret_key: str = Field("1234", alias="SESSION_SECRET_KEY")
    localhost_client_origin: str = Field("http://localhost:5173")

    @property
    def allowed_origins(self) -> list[str]:
        origins = {origin.strip() for origin in self.allowed_origins_str.split(",")}
        if self.MODE in (APIModeEnum.LOCAL, APIModeEnum.DEV, APIModeEnum.STAGE):
            origins.add(self.localhost_client_origin)
        return sorted(origins)

    def get_full_static_url(self, path: str) -> str:
        """Added static_files_host to passed path to get full URL"""
        return urljoin(self.static_files_host, path)
