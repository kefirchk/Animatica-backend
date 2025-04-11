from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class DBConfig(BaseSettings):
    DB_HOST: str = Field(..., alias="DB_HOST")
    DB_PORT: str = Field(..., alias="DB_PORT")
    DB_NAME: str = Field(..., alias="DB_NAME")
    DB_USER: str = Field(..., alias="DB_USER")
    DB_PASS: SecretStr = Field(..., alias="DB_PASS")
    DB_DRIVER: str = Field("postgresql+asyncpg")

    model_config = SettingsConfigDict(env_file="../env/db.env")

    @property
    def db_conn_url(self):
        encoded_password = self.DB_PASS.get_secret_value()
        connection_url = (
            f"{self.DB_DRIVER}://"
            f"{self.DB_USER}:"
            f"{encoded_password}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        return connection_url
