class ModelException(Exception):
    """Base exception for all errors related to ML model"""


class ModelConnectionException(ModelException):
    """Unable to connect to or load the ML model"""


class ModelNotTrainedException(ModelException):
    """Model is used without being properly trained"""


class PermissionException(Exception):
    """The API is not allowed for a user."""


class DataBaseException(Exception):
    """Base exception for all errors related to Database"""


class ConnectionError(DataBaseException):
    """This exception will be raised if unable to connect to database or upon connection drop"""


class InternalError(DataBaseException):
    """Raised upon database internal issue"""


class NoSuchItem(DataBaseException):
    """This exception will be raised in 'get' method if there is no such record in database"""


class BadRequest(Exception):
    """Request contains invalid parameters"""


class AuthException(Exception):
    """Base exception for all errors related to authorization"""


class InvalidCredentialsException(AuthException):
    """Raised when provided credentials (email/password) are invalid."""


class UserExistsException(AuthException):
    """Raised when attempting to create a user with an email that already exists."""


class ExpiredTokenException(AuthException):
    """Raised when the token used for authentication has expired."""


class UnauthorizedAccessError(AuthException):
    """Raised when the user is not authorized to access certain resources or perform certain actions."""


class RateLimitExceededError(AuthException):
    """Raised when the rate limit for authentication requests has been exceeded."""


class InvalidTokenException(AuthException):
    """Raised when the provided token is invalid or cannot be recognized."""
