from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.entities.subscription import (
    SubscriptionPricing,
    SuggestedSubscription,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.repositories import SubscriptionRepository
from starlette.responses import JSONResponse


class GetSuggestedSubscriptionsUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo

    class Response(ResponseModel):
        subscriptions: list[SuggestedSubscription]

    def __init__(self):
        self.subscription_repository = SubscriptionRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.subscription_repository as repository:
                subscriptions_data = await repository.get_suggested()
                subscriptions = [
                    SuggestedSubscription(
                        subscription_type_id=s.id,
                        subscription_type_name=s.name,
                        features=[f.feature.description for f in s.features],
                        pricing=SubscriptionPricing(
                            price=round(s.price, 2),
                            discount=round(s.discount, 2),
                            currency=s.currency,
                        ),
                        total_credits=s.total_credits,
                        duration_days=s.duration_days,
                    )
                    for s in subscriptions_data
                ]

            return ResponseSuccess.build(self.Response(subscriptions=subscriptions))
        except Exception as exc:
            return ResponseFailure.build(exc)
