from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class MLEngineConfig(BaseSettings):
    BASE_URL: str = Field(..., alias="ML_ENGINE_BASE_URL")
    ML_ENGINE_KEY: str = Field(..., alias="ML_ENGINE_KEY")
    ML_ENGINE_KEY_HEADER: str = Field("X-ML-Engine-Key", alias="ML_ENGINE_KEY_HEADER")

    model_config = SettingsConfigDict(env_file="../env/ml_engine.env")
