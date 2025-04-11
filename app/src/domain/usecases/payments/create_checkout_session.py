import logging

from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.configs import APIConfig
from src.infrastructure.repositories.stripe_repository import StripeRepository
from starlette.responses import JSONResponse

log = logging.getLogger(__name__)


class CreateCheckoutSessionUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo
        price_id: str

    class Response(ResponseModel):
        checkout_session: dict

    def __init__(self):
        self.redirect_url = f"{APIConfig().FRONTEND_BASE_URL}/pricing"
        self.stripe_repository = StripeRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            log.info(f"Creating checkout session with price_id: {request.price_id}")

            params = {
                "payment_method_types": ["card"],
                "line_items": [{"price": request.price_id, "quantity": 1}],
                "mode": "payment",
                "success_url": f"{self.redirect_url}?success=true",
                "cancel_url": f"{self.redirect_url}?canceled=true",
            }
            checkout_session = await self.stripe_repository.create_checkout_session(params)

            return ResponseSuccess.build(self.Response(checkout_session=checkout_session))
        except Exception as exc:
            return ResponseFailure.build(exc)
