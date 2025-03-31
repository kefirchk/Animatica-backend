from datetime import datetime

from pydantic import BaseModel, Field
from src.domain.entities.enums import SuggestedSubscriptionTypeEnum


class SubscriptionPricing(BaseModel):
    price: float = Field(ge=0)
    currency: str = Field(min_length=3, max_length=3)
    discount: float | None = Field(None, ge=0, le=100)


class SuggestedSubscription(BaseModel):
    subscription_type_id: int = Field(gt=0)
    subscription_type_name: SuggestedSubscriptionTypeEnum
    total_credits: int | None = Field(gt=0)
    duration_days: int | None = Field(gt=0)
    features: list[str]
    pricing: SubscriptionPricing


class UserSubscription(BaseModel):
    user_subscription_id: int = Field(gt=0)
    subscription_type_id: int = Field(gt=0)
    remaining_credits: int | None = None
    expired_at: str | None = None
