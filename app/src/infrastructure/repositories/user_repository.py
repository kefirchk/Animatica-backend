from sqlalchemy import select
from src.domain.interfaces import IDBRepository
from src.infrastructure.models.models import User
from src.infrastructure.services.security import PasswordService


class UserRepository(IDBRepository):
    async def create_user(self, username: str, password: str) -> None:
        """
        Creates a new user with a hashed password.

        Parameters:
            username (str): The username of the user.
            password (str): The plaintext password to be hashed.
        """
        user = User(
            username=username,
            hashed_password=PasswordService.hash_password(password),
        )
        self.async_session.add(user)

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieves a user by username.

        This asynchronous method fetches a user from the database that matches the specified username.

        Parameters:
            username (str):
                The username of the user to retrieve.

        Returns:
            User:
                The user object or None if no such user exists.
        """
        query = select(User).where(User.username == username)
        result = await self.async_session.execute(query)
        return result.scalars().first()
