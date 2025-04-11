from typing import Annotated

from fastapi import Body, Depends
from pydantic import SecretStr
from src.domain.usecases.auth import UserLoginUseCase, UserSignUpUseCase
from src.infrastructure.api import APIRouter

router = APIRouter()


@router.post("/login")
async def login(
    use_case: Annotated[UserLoginUseCase, Depends(UserLoginUseCase)],
    username: str = Body(..., min_length=3),
    password: SecretStr = Body(..., min_length=8),
):
    return await use_case.execute(use_case.Request(username=username, password=password.get_secret_value()))


@router.post("/signup")
async def signup(
    use_case: Annotated[UserSignUpUseCase, Depends(UserSignUpUseCase)],
    username: str = Body(..., min_length=3),
    password: SecretStr = Body(..., min_length=8),
):
    return await use_case.execute(use_case.Request(username=username, password=password.get_secret_value()))
