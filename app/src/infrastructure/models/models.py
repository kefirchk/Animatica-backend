from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Float, ForeignKey, Integer, String, and_, not_, or_
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from src.domain.entities.enums import SubscriptionTypeEnum


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)


class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[SubscriptionTypeEnum] = mapped_column(
        SQLAlchemyEnum(SubscriptionTypeEnum), nullable=False, unique=True
    )
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    discount: Mapped[float | None] = mapped_column(Float(precision=2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    total_credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration_days: Mapped[int | None] = mapped_column(Integer, nullable=True, comment="Duration in days")

    features: Mapped[list["SubscriptionTypeFeatures"]] = relationship(
        "SubscriptionTypeFeatures", back_populates="subscription_type", lazy="select"
    )

    __table_args__ = (
        CheckConstraint(
            or_(total_credits.is_not(None), duration_days.is_not(None)), name="subscription_type_check_not_both_null"
        ),
        CheckConstraint(
            not_(and_(total_credits.is_not(None), duration_days.is_not(None))),
            name="subscription_type_check_not_both_not_null",
        ),
    )


class SubscriptionFeature(Base):
    __tablename__ = "subscription_feature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)

    subscription_types: Mapped[list["SubscriptionTypeFeatures"]] = relationship(
        "SubscriptionTypeFeatures", back_populates="feature", lazy="select"
    )


class SubscriptionTypeFeatures(Base):
    __tablename__ = "subscription_type_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), nullable=False)
    subscription_feature_id: Mapped[int] = mapped_column(ForeignKey("subscription_feature.id"), nullable=False)

    subscription_type: Mapped["SubscriptionType"] = relationship("SubscriptionType", back_populates="features")

    feature: Mapped["SubscriptionFeature"] = relationship("SubscriptionFeature", back_populates="subscription_types")


class UserSubscription(Base):
    __tablename__ = "user_subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    remaining_credits: Mapped[int | None] = mapped_column(Integer, nullable=True)
    expired_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    __table_args__ = (
        CheckConstraint(
            or_(
                remaining_credits.is_not(None),
                expired_at.is_not(None),
            ),
            name="user_subscription_check_not_both_null",
        ),
        CheckConstraint(
            not_(
                and_(
                    remaining_credits.is_not(None),
                    expired_at.is_not(None),
                )
            ),
            name="user_subscription_check_not_both_not_null",
        ),
    )
