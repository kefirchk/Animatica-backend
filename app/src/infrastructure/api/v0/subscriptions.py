from typing import Annotated

from fastapi import Depends, Path
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.subscriptions import (
    GetCurrentSubscriptionUseCase,
    GetSuggestedSubscriptionsUseCase,
    SubscribeUseCase,
    UnsubscribeUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security import JWTBearer

router = APIRouter()


@router.post("/{subscription_type_id}/subscribe")
async def subscribe(
    use_case: Annotated[SubscribeUseCase, Depends(SubscribeUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
    subscription_type_id: int = Path(
        ..., gt=0, description="Unique identifier of the subscription type the user wants to subscribe to"
    ),
):
    return await use_case.execute(use_case.Request(user=user, subscription_type_id=subscription_type_id))


@router.delete("/unsubscribe")
async def unsubscribe(
    use_case: Annotated[UnsubscribeUseCase, Depends(UnsubscribeUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/suggested")
async def get_suggested_subscriptions(
    use_case: Annotated[GetSuggestedSubscriptionsUseCase, Depends(GetSuggestedSubscriptionsUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/current")
async def get_current_subscription(
    use_case: Annotated[GetCurrentSubscriptionUseCase, Depends(GetCurrentSubscriptionUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
):
    return await use_case.execute(use_case.Request(user=user))
