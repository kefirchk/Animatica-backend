from src.infrastructure.api.utils import APIRouter

from .auth import router as auth_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# router.include_router(ml_router, prefix="/ml", tags=["ML"])
