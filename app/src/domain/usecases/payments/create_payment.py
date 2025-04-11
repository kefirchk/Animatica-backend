from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.configs import APIConfig
from src.infrastructure.exceptions.exceptions import (
    StripeException,
    StripePaymentException,
)
from src.infrastructure.repositories import (
    SubscriptionRepository,
    UserRepository,
)
from src.infrastructure.repositories.stripe_repository import StripeRepository
from starlette.responses import JSONResponse


class CreatePaymentUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo
        session_id: str
        product_id: str

    class Response(ResponseModel):
        remaining_queries: int
        session_id: str

    def __init__(self):
        self.redirect_url = f"{APIConfig().FRONTEND_BASE_URL}/pricing"
        self.stripe_repository = StripeRepository()
        self.subscription_repository = SubscriptionRepository()
        self.user_repository = UserRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            product = await self.stripe_repository.get_product(request.product_id)
            checkout_session = await self.stripe_repository.get_checkout_session(request.session_id)
            if checkout_session.payment_status != "paid":
                raise StripePaymentException()

            queries_amount = int(product.metadata.get("queries", 0))
            if queries_amount <= 0:
                raise StripeException("Invalid queries amount in product metadata", 400)

            async with self.user_repository as repository:
                user = await repository.get_user_by_username(request.user.sub_id)
                user_id = user.id

            async with self.subscription_repository as repository:
                subscription = await repository.get_one_by_user_id(user_id=user_id)
                if subscription:
                    subscription = await repository.update_one(
                        existing_subscription=subscription,
                        queries=queries_amount,
                    )
                else:
                    subscription = await repository.add_one(
                        user_id=user_id,
                        queries=queries_amount,
                    )
                remaining_queries = subscription.remaining_queries

            return ResponseSuccess.build(
                self.Response(remaining_queries=remaining_queries, session_id=checkout_session.id)
            )
        except Exception as exc:
            return ResponseFailure.build(exc)
