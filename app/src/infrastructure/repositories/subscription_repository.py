from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.domain.interfaces import IDBRepository
from src.infrastructure.models.models import (
    SubscriptionType,
    SubscriptionTypeFeatures,
    UserSubscription,
)


class SubscriptionRepository(IDBRepository):
    async def get_suggested(self):
        query = (
            select(SubscriptionType)
            .options(joinedload(SubscriptionType.features).joinedload(SubscriptionTypeFeatures.feature))
            .order_by(SubscriptionType.id)
        )
        result = await self.async_session.execute(query)
        return result.unique().scalars().all()

    async def get_one_by_id(self, subscription_type_id: int) -> SubscriptionType | None:
        query = select(SubscriptionType).where(SubscriptionType.id == subscription_type_id)
        result = await self.async_session.execute(query)
        return result.scalar_one_or_none()

    async def get_one_for_user(self, user_id: int) -> UserSubscription | None:
        stmt = select(UserSubscription).where(UserSubscription.user_id == user_id)
        result = await self.async_session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_one_for_user(self, subscription_type_id: int, user_id: int) -> UserSubscription:
        subscription_type = await self.get_one_by_id(subscription_type_id=subscription_type_id)

        user_subscription = UserSubscription(
            subscription_type_id=subscription_type_id,
            user_id=user_id,
            remaining_credits=subscription_type.total_credits,
            expired_at=(
                datetime.utcnow() + timedelta(days=subscription_type.duration_days)
                if subscription_type.duration_days
                else None
            ),
        )
        self.async_session.add(user_subscription)
        await self.async_session.flush()
        return user_subscription

    async def update_one_for_user(
        self, existing_subscription: UserSubscription, subscription_type_id: int
    ) -> UserSubscription:
        subscription_type = await self.get_one_by_id(subscription_type_id=subscription_type_id)

        existing_subscription.subscription_type_id = subscription_type_id
        existing_subscription.remaining_credits = subscription_type.total_credits
        existing_subscription.expired_at = (
            datetime.utcnow() + timedelta(days=subscription_type.duration_days)
            if subscription_type.duration_days
            else None
        )

        await self.async_session.flush()
        return existing_subscription

    async def delete_one_for_user(self, existing_subscription: UserSubscription) -> None:
        await self.async_session.delete(existing_subscription)
        await self.async_session.flush()
        return None
