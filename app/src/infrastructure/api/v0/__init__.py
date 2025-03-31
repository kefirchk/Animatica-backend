from src.infrastructure.api.utils import APIRouter

from .auth import router as auth_router
from .generating import router as generating_router
from .subscriptions import router as subscriptions_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(generating_router, prefix="/generating", tags=["Generating"])
router.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions"])
