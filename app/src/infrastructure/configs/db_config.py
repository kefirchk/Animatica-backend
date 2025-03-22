from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings


class DBConfig(BaseSettings):
    DB_HOST: str = Field("localhost")
    DB_PORT: str = Field("5432")
    DB_NAME: str = Field("animatica")
    DB_USER: str = Field("postgres")
    DB_PASSWORD: SecretStr = Field("postgres")
    DB_DRIVER: str = Field("postgresql+asyncpg")

    @property
    def DB_CONN_URL(self):
        encoded_password = self.DB_PASSWORD.get_secret_value()
        connection_url = (
            f"{self.DB_DRIVER}://"
            f"{self.DB_USER}:"
            f"{encoded_password}@"
            f"{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )
        return connection_url
