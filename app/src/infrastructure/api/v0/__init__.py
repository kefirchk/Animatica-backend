from src.infrastructure.api.utils import APIRouter

from .animation import router as animation_router
from .auth import router as auth_router
from .payments import router as payments_router
from .subscriptions import router as subscriptions_router

router = APIRouter()
router.include_router(animation_router, prefix="/animation", tags=["Animation"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(payments_router, prefix="/payments", tags=["Payments"])
router.include_router(subscriptions_router, prefix="/subscriptions", tags=["Subscriptions"])
