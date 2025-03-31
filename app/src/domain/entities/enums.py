from enum import StrEnum


class APIModeEnum(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


class LogLevelEnum(StrEnum):
    INFO = "info"
    DEBUG = "debug"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class SubscriptionTypeEnum(StrEnum):
    TRIAL = "trial"
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"


class SuggestedSubscriptionTypeEnum(StrEnum):
    BASIC = SubscriptionTypeEnum.BASIC
    STANDARD = SubscriptionTypeEnum.STANDARD
    PREMIUM = SubscriptionTypeEnum.PREMIUM


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
