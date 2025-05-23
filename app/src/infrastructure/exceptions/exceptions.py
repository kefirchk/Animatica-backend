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


class StripeException(Exception):
    """Base exception for Stripe product related errors."""


class StripePaymentException(StripeException):
    """Raised when there are issues with payment processing."""


class MLEngineException(Exception):
    """Base exception for all errors related to ML Engine"""
