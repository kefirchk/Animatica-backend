from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
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


class SubscriptionFeature(Base):
    __tablename__ = "subscription_feature"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    description: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


class SubscriptionTypeFeatures(Base):
    __tablename__ = "subscription_type_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), nullable=False)
    subscription_feature_id: Mapped[int] = mapped_column(ForeignKey("subscription_feature.id"), nullable=False)


class Subscription(Base):
    __tablename__ = "subscription"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    subscription_type_id: Mapped[int] = mapped_column(ForeignKey("subscription_type.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
