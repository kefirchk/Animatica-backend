from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.configs import StripeConfig
from src.infrastructure.repositories.stripe_repository import StripeRepository
from starlette.responses import JSONResponse


class GetLimitedSubscriptionsUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo

    class Response(ResponseModel):
        object: str
        data: list[dict]
        has_more: bool
        public_key: str

    def __init__(self):
        self.stripe_repository = StripeRepository()
        self.stripe_config = StripeConfig()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            products = await self.stripe_repository.get_products()
            return ResponseSuccess.build(self.Response(**products, public_key=self.stripe_config.PUBLIC_KEY))
        except Exception as exc:
            return ResponseFailure.build(exc)
