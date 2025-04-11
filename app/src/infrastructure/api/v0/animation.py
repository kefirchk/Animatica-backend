from typing import Annotated

from fastapi import Depends
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.animation import (
    AnimateImageByVideoUseCase,
    AnimateImageInRealTimeUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security.jwt_bearer import JWTBearer

router = APIRouter()


@router.post("/video")
async def animate_image_by_video(
    use_case: Annotated[AnimateImageByVideoUseCase, Depends(AnimateImageByVideoUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/real-time")
async def animate_image_in_real_time(
    use_case: Annotated[AnimateImageInRealTimeUseCase, Depends(AnimateImageInRealTimeUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))
