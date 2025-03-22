import asyncio
import time
from datetime import datetime

import asyncpg
from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker
from src.domain.interfaces import IDBRepository
from src.infrastructure.configs import DBConfig
from src.infrastructure.models.models import User
from src.infrastructure.services.security import hash_password

engine = create_async_engine(
    DBConfig().DB_CONN_URL,
    pool_size=10,
    max_overflow=20,
)
SessionFactory = sessionmaker(bind=engine, class_=AsyncSession)


class DBRepository(IDBRepository):
    async def __aenter__(self) -> "DBRepository":
        self.async_session = SessionFactory()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_val:
            await self.async_session.rollback()
            await self.async_session.close()
            if exc_type == OperationalError:
                raise ConnectionError("Could not connect to DataBase instance")
            return
        await self.async_session.commit()
        await self.async_session.close()

    @staticmethod
    def verify_db_connection() -> bool:
        config = DBConfig()

        async def attempt_connection():
            return await asyncpg.connect(
                database=config.name,
                user=config.user,
                password=config.password.get_secret_value(),
                host=config.hostname,
                port=config.port,
            )

        for _ in range(5):
            try:
                time.sleep(1)
                asyncio.run(attempt_connection())
                return True
            except OperationalError:
                continue
        return False

    async def create_user(self, sub: str, name: str, email: str, password: str | None = None) -> None:
        """
        Creates a new user with a hashed password.

        Parameters:
            sub (str): The unique identifier of the user from the authentication provider.
            name (str): The name of the user.
            email (str): The email of the user.
            password (str | None): The plaintext password to be hashed.
        """
        user = User(
            username=name,
            email=email,
            sub=sub,
            hashed_password=hash_password(password) if password else None,
            created_at=datetime.now(),
            is_active=True,
        )
        self.async_session.add(user)

    async def get_user(self, user_name) -> User:
        """
        Retrieves a user by username.

        This asynchronous method fetches a user from the database that matches the specified username.

        Parameters:
            user_name (str):
                The username of the user to retrieve.

        Returns:
            User:
                The user object or None if no such user exists.
        """
        user_query = select(User).where(User.username == user_name)
        user_result = await self.async_session.execute(user_query)
        return user_result.scalar()

    async def get_user_by_sub(self, sub: str) -> User:
        """
        Retrieves a user by their unique sub identifier.

        This asynchronous method fetches a user from the database that matches the specified sub identifier.

        Parameters:
            sub (str):
                The unique sub identifier of the user to retrieve.

        Returns:
            User:
                The user object or None if no such user exists.
        """
        user_query = select(User).where(User.sub == sub)
        user_result = await self.async_session.execute(user_query)
        return user_result.scalar()

    async def get_user_by_email(self, email: str) -> User:
        """
        Retrieves a user by their email address.

        This asynchronous method fetches a user from the database that matches the specified email address.

        Parameters:
            email (str):
                The email address of the user to retrieve.

        Returns:
            User:
                The user object or None if no such user exists.
        """
        user_query = select(User).where(User.email == email)
        user_result = await self.async_session.execute(user_query)
        return user_result.scalar()
