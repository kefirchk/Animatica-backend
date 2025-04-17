import logging
from contextlib import asynccontextmanager

import src
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.domain.entities.enums import LogLevelEnum
from src.infrastructure.api import router as api_router
from src.infrastructure.configs import APIConfig
from src.infrastructure.exceptions.handlers import (
    app_exception_handler,
    exception_handlers,
)
from starlette.middleware.sessions import SessionMiddleware

logging.basicConfig(format="[PID:%(process)d] %(pathname)s:%(lineno)d %(message)s", level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


app = FastAPI(
    title=f"{APIConfig().MODE.capitalize()} Animatica Backend API",
    description="This API is designed for the Animatica application.",
    swagger_ui_parameters={"displayRequestDuration": True},
    version=src.__version__,
    debug=(APIConfig().LOG_LEVEL == LogLevelEnum.DEBUG),
)

app.add_middleware(SessionMiddleware, secret_key=APIConfig().SESSION_SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=APIConfig().allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

for exc_type in exception_handlers:
    app.add_exception_handler(exc_type, app_exception_handler)
