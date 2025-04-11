from pydantic import BaseModel, Field


class Subscription(BaseModel):
    subscription_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    remaining_queries: int = Field(ge=0)
