from typing import Annotated

from fastapi import Depends
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.subscriptions import (
    GetCurrentSubscriptionUseCase,
    GetLimitedSubscriptionsUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security import JWTBearer

router = APIRouter()


@router.get("/current")
async def get_current_subscription(
    use_case: Annotated[GetCurrentSubscriptionUseCase, Depends(GetCurrentSubscriptionUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/limited")
async def get_limited_subscriptions(
    use_case: Annotated[GetLimitedSubscriptionsUseCase, Depends(GetLimitedSubscriptionsUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
):
    return await use_case.execute(use_case.Request(user=user))
