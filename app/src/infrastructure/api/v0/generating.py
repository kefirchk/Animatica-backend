from typing import Annotated

from fastapi import Depends, File, UploadFile
from src.domain.usecases.generating import (
    GenerateImageByTextUseCase,
    GenerateRandomImageUseCase,
    GenerateRandomVideoUseCase,
    GenerateVideoByImageUseCase,
    GenerateVideoByTextUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.auth import JWTBearer, UserAuthInfo

router = APIRouter()


@router.get("/image-to-video")
async def generate_video_by_image(
    use_case: Annotated[GenerateVideoByImageUseCase, Depends(GenerateVideoByImageUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=False))],
    image: UploadFile = File(...),
):
    image_bytes = await image.read()
    return await use_case.execute(use_case.Request(user=user, image=image_bytes))


@router.get("/text-to-video")
async def generate_video_by_text(
    use_case: Annotated[GenerateVideoByTextUseCase, Depends(GenerateVideoByTextUseCase)],
    text: str,
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user, text=text))


@router.get("/text-to-image")
async def generate_image_by_text(
    use_case: Annotated[GenerateImageByTextUseCase, Depends(GenerateImageByTextUseCase)],
    text: str,
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user, text=text))


@router.get("/random-image")
async def generate_random_video(
    use_case: Annotated[GenerateRandomImageUseCase, Depends(GenerateRandomImageUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/random-video")
async def generate_random_video(
    use_case: Annotated[GenerateRandomVideoUseCase, Depends(GenerateRandomVideoUseCase)],
    user: Annotated[UserAuthInfo, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))
