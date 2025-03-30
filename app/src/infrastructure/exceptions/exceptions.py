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
