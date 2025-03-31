from src.domain.entities.auth import UserAuthInfo
from src.domain.entities.request import RequestModel
from src.domain.entities.response import (
    ResponseFailure,
    ResponseModel,
    ResponseSuccess,
)
from src.domain.interfaces import IUseCase
from src.infrastructure.repositories import (
    SubscriptionRepository,
    UserRepository,
)
from starlette.responses import JSONResponse


class UnsubscribeUseCase(IUseCase):
    class Request(RequestModel):
        user: UserAuthInfo

    class Response(ResponseModel):
        pass

    def __init__(self):
        self.user_repository = UserRepository()
        self.subscription_repository = SubscriptionRepository()

    async def execute(self, request: Request) -> JSONResponse:
        try:
            async with self.user_repository as repository:
                user = await repository.get_user_by_username(username=request.user.sub_id)
                user_id = user.id

            async with self.subscription_repository as repository:
                existing_subscription = await repository.get_one_for_user(user_id=user_id)
                if existing_subscription:
                    await repository.delete_one_for_user(
                        existing_subscription=existing_subscription,
                    )

            return ResponseSuccess.build(self.Response())
        except Exception as exc:
            return ResponseFailure.build(exc)
