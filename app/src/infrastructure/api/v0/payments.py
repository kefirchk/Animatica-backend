from typing import Annotated

from fastapi import Depends, Query
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.payments import (
    CreateCheckoutSessionUseCase,
    CreatePaymentUseCase,
    GetCheckoutSessionUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security import JWTBearer

router = APIRouter()


@router.get("/checkout-session")
async def get_checkout_session(
    use_case: Annotated[GetCheckoutSessionUseCase, Depends(GetCheckoutSessionUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
    session_id: str = Query(..., description="Session ID of Stripe checkout session"),
):
    return await use_case.execute(use_case.Request(user=user, session_id=session_id))


@router.post("/checkout-session")
async def create_checkout_session(
    use_case: Annotated[CreateCheckoutSessionUseCase, Depends(CreateCheckoutSessionUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
    price_id: str = Query(..., description="Price ID of Stripe checkout session"),
):
    return await use_case.execute(use_case.Request(user=user, price_id=price_id))


@router.post("")
async def create_payment(
    use_case: Annotated[CreatePaymentUseCase, Depends(CreatePaymentUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
    session_id: str = Query(..., description="Session ID of Stripe checkout session"),
    product_id: str = Query(..., description="Payment Stripe Product ID"),
):
    return await use_case.execute(use_case.Request(user=user, session_id=session_id, product_id=product_id))
