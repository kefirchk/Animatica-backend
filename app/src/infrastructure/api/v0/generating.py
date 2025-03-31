from typing import Annotated

from fastapi import Depends, File, UploadFile
from src.domain.entities.auth import UserAuthInfo
from src.domain.usecases.generating import (
    GenerateImageByTextUseCase,
    GenerateRandomImageUseCase,
    GenerateRandomVideoUseCase,
    GenerateVideoByImageUseCase,
    GenerateVideoByTextUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.security import JWTBearer

router = APIRouter()


@router.post("/image-to-video")
async def generate_video_by_image(
    use_case: Annotated[GenerateVideoByImageUseCase, Depends(GenerateVideoByImageUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
    image: UploadFile = File(...),
):
    image_bytes = await image.read()
    return await use_case.execute(use_case.Request(user=user, image=image_bytes))


@router.get("/text-to-video")
async def generate_video_by_text(
    use_case: Annotated[GenerateVideoByTextUseCase, Depends(GenerateVideoByTextUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
    text: str,
):
    return await use_case.execute(use_case.Request(user=user, text=text))


@router.get("/text-to-image")
async def generate_image_by_text(
    use_case: Annotated[GenerateImageByTextUseCase, Depends(GenerateImageByTextUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
    text: str,
):
    return await use_case.execute(use_case.Request(user=user, text=text))


@router.get("/random-image")
async def generate_random_video(
    use_case: Annotated[GenerateRandomImageUseCase, Depends(GenerateRandomImageUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))


@router.get("/random-video")
async def generate_random_video(
    use_case: Annotated[GenerateRandomVideoUseCase, Depends(GenerateRandomVideoUseCase)],
    user: Annotated[UserAuthInfo | None, Depends(JWTBearer(auto_error=False))],
):
    return await use_case.execute(use_case.Request(user=user))
