from src.domain.entities.user import UserRead
from src.infrastructure.repositories import UserRepository
from src.infrastructure.services.security.password import PasswordService


class AuthService:
    def __init__(self) -> None:
        self.user_repository = UserRepository()
        self.password_service = PasswordService()

    async def authenticate_user(self, username: str, password: str) -> UserRead | None:
        async with self.user_repository as repository:
            user = await repository.get_user_by_username(username)

            if not user or not self.password_service.verify_password(password, user.hashed_password):
                return None

            return UserRead.model_validate(user)
