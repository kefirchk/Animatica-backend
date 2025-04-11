from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.repositories.stripe_repository import StripeRepository
from starlette.responses import JSONResponse


class GetCheckoutSessionUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo
        session_id: str

    class Response(ResponseModel):
        checkout_session: dict

    def __init__(self):
        self.stripe_repository = StripeRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            checkout_session = await self.stripe_repository.get_checkout_session(request.session_id)
            return ResponseSuccess.build(self.Response(checkout_session=checkout_session))
        except Exception as exc:
            return ResponseFailure.build(exc)
