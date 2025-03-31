class AuthException(Exception):
    """Base exception for all errors related to authorization"""


class InvalidCredentialsException(AuthException):
    """Raised when provided credentials (username/password) are invalid."""


class UserAlreadyExistsException(AuthException):
    """Raised when attempting to create a user with an email that already exists."""


class ExpiredTokenException(AuthException):
    """Raised when the token used for authentication has expired."""


class InvalidTokenException(AuthException):
    """Raised when the provided token is invalid or cannot be recognized."""


class NotFoundException(Exception):
    """Base exception for all not found errors"""

    entity_name: str = "Entity"

    def __init__(self, entity_id=None):
        self.entity_id = entity_id
        message = f"{self.entity_name} not found"
        if entity_id is not None:
            message += f" with id {entity_id}"
        super().__init__(message)


class SubscriptionTypeNotFound(NotFoundException):
    """Raised when subscription type is not found"""

    entity_name = "Subscription type"
