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


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
