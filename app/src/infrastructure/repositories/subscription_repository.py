from sqlalchemy import select
from src.domain.interfaces import IDBRepository
from src.infrastructure.models.models import Subscription


class SubscriptionRepository(IDBRepository):
    async def get_one_by_user_id(self, user_id: int) -> Subscription | None:
        stmt = select(Subscription).where(Subscription.user_id == user_id)
        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_one(self, user_id: int, queries: int) -> Subscription:
        subscription = Subscription(user_id=user_id, remaining_queries=queries)
        self.async_session.add(subscription)
        await self.async_session.flush()
        return subscription

    async def update_one(self, existing_subscription: Subscription, queries: int) -> Subscription:
        existing_subscription.remaining_queries += queries
        await self.async_session.flush()
        return existing_subscription
