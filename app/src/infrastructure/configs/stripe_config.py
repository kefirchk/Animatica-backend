import stripe
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class StripeConfig(BaseSettings):
    PUBLIC_KEY: str = Field(..., alias="STRIPE_PUBLIC_KEY")
    SECRET_KEY: str = Field(..., alias="STRIPE_SECRET_KEY")

    model_config = SettingsConfigDict(env_file="../env/stripe.env")


stripe.api_key = StripeConfig().SECRET_KEY
