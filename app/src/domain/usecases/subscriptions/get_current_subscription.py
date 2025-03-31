from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.entities.subscription import UserSubscription
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
        user_subscription: UserSubscription | None

    def __init__(self):
        self.user_repository = UserRepository()
        self.subscription_repository = SubscriptionRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.user_repository as repository:
                user = await repository.get_user_by_username(username=request.user.sub_id)
                user_id = user.id

            user_subscription = None
            async with self.subscription_repository as repository:
                current_subscription = await repository.get_one_for_user(user_id=user_id)
                if current_subscription:
                    user_subscription = UserSubscription(
                        user_subscription_id=current_subscription.id,
                        subscription_type_id=current_subscription.subscription_type_id,
                        remaining_credits=current_subscription.remaining_credits,
                        expired_at=(
                            current_subscription.expired_at.isoformat() if current_subscription.expired_at else None
                        ),
                    )

            return ResponseSuccess.build(self.Response(user_subscription=user_subscription))
        except Exception as exc:
            return ResponseFailure.build(exc)
