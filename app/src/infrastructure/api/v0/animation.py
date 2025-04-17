from typing import Annotated

from fastapi import Depends, File, UploadFile
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.animation import AnimateImageByVideoUseCase
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security.jwt_bearer import JWTBearer

router = APIRouter()


@router.post("/video")
async def animate_image_by_video(
    use_case: Annotated[AnimateImageByVideoUseCase, Depends(AnimateImageByVideoUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=True))],
    source_image: UploadFile = File(...),
    driving_video: UploadFile = File(...),
):
    return await use_case.execute(use_case.Request(user=user, source_image=source_image, driving_video=driving_video))
