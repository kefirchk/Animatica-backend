from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.entities.subscription import Subscription
from src.domain.interfaces import IUseCase
from src.infrastructure.repositories import (
    SubscriptionRepository,
    UserRepository,
)
from starlette.responses import JSONResponse


class GetCurrentSubscriptionUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo

    class Response(ResponseModel):
        subscription: Subscription | None

    def __init__(self):
        self.user_repository = UserRepository()
        self.subscription_repository = SubscriptionRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.user_repository as repository:
                user = await repository.get_user_by_username(username=request.user.sub_id)
                user_id = user.id

            subscription = None
            async with self.subscription_repository as repository:
                current_subscription = await repository.get_one_by_user_id(user_id=user_id)
                if current_subscription:
                    subscription = Subscription(
                        subscription_id=current_subscription.id,
                        user_id=current_subscription.id,
                        remaining_queries=current_subscription.remaining_queries,
                    )

            return ResponseSuccess.build(self.Response(subscription=subscription))
        except Exception as exc:
            return ResponseFailure.build(exc)
