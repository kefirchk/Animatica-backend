from enum import StrEnum

from pydantic import BaseModel


class UserLoginEntity(BaseModel):
    email: str
    password: str


class UserSignUpEntity(BaseModel):
    name: str
    password: str
    email: str


class UserVerifyEntity(BaseModel):
    username: str
    confirmation_code: str


class ForgotPasswordEntity(BaseModel):
    email: str


class ResetPasswordEntity(BaseModel):
    token: str
    password: str


class RefreshTokenEntity(BaseModel):
    refresh_token: str


class InvalidateTokenEntity(BaseModel):
    refresh_token: str


class VerifyTokenEntity(BaseModel):
    id_token: str


class RefreshTokensEntity(BaseModel):
    refresh_token: str


class IdentityProviderName(StrEnum):
    vk = "vk"
    google = "google"
    yandex = "yandex"
