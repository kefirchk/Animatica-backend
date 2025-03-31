import logging
import traceback

from fastapi import Request, status
from pydantic import ValidationError
from src.domain.entities.enums import APIModeEnum
from src.infrastructure.configs import APIConfig
from src.infrastructure.exceptions.exceptions import *
from starlette.responses import JSONResponse

log = logging.getLogger(__name__)


exception_handlers: dict[type[Exception], callable] = {
    ExpiredTokenException: lambda x: (status.HTTP_401_UNAUTHORIZED, "Expired token"),
    InvalidCredentialsException: lambda x: (status.HTTP_401_UNAUTHORIZED, "Invalid credentials"),
    InvalidTokenException: lambda x: (status.HTTP_401_UNAUTHORIZED, "Invalid token"),
    UserAlreadyExistsException: lambda x: (status.HTTP_409_CONFLICT, "User already exists"),
    ValidationError: lambda x: (status.HTTP_422_UNPROCESSABLE_ENTITY, x.errors()),
}


def handle_exception(exc: Exception) -> tuple[str, int]:
    if handler := exception_handlers.get(type(exc)):
        status_code, message = handler(exc)
    else:
        status_code, message = status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal server error"

    log.error(message, exc_info=True)

    if APIConfig().MODE != APIModeEnum.PROD:
        traceback_text = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
        message = f"{message}: {str(exc)}\n{traceback_text}"

    return message, status_code


async def app_exception_handler(request: Request, exc: Exception):
    message, status_code = handle_exception(exc)
    return JSONResponse(status_code=status_code, content={"detail": message})
