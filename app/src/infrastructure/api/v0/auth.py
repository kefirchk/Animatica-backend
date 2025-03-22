from typing import Annotated

from fastapi import Depends
from src.domain.entities.auth import (
    ForgotPasswordEntity,
    RefreshTokensEntity,
    ResetPasswordEntity,
    UserLoginEntity,
    UserSignUpEntity,
)
from src.domain.usecases.auth import (
    ForgotPasswordUseCase,
    RefreshTokensUseCase,
    ResetPasswordUseCase,
    UserLoginUseCase,
    UserSignUpUseCase,
)
from src.infrastructure.api import APIRouter
from src.infrastructure.services.auth import JWTBearer

router = APIRouter()


@router.post("/login", response_model=UserLoginUseCase.Response)
async def login(payload: UserLoginEntity, use_case: Annotated[UserLoginUseCase, Depends(UserLoginUseCase)]):
    return await use_case.execute(use_case.Request(username=payload.email, password=payload.password))


@router.post("/signup")
async def signup(
    payload: UserSignUpEntity,
    use_case: Annotated[UserSignUpUseCase, Depends(UserSignUpUseCase)],
):
    return await use_case.execute(
        use_case.Request(
            email=payload.email,
            password=payload.password,
            name=payload.name,
        )
    )


@router.post("/refresh-tokens", response_model=RefreshTokensUseCase.Response)
async def refresh_tokens(
    entity: RefreshTokensEntity,
    use_case: Annotated[RefreshTokensUseCase, Depends(RefreshTokensUseCase)],
):
    return await use_case.execute(use_case.Request(refresh_token=entity.refresh_token))


@router.post("/forgot-password")
async def forgot_password(
    payload: ForgotPasswordEntity,
    use_case: Annotated[ForgotPasswordUseCase, Depends(ForgotPasswordUseCase)],
):
    return await use_case.execute(use_case.Request(email=payload.email))


@router.post("/reset-password")
async def reset_password(
    payload: ResetPasswordEntity,
    use_case: Annotated[ResetPasswordUseCase, Depends(ResetPasswordUseCase)],
):
    return await use_case.execute(use_case.Request(token=payload.token, password=payload.password))
