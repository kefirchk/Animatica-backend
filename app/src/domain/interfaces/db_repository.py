from abc import ABC

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm.session import sessionmaker
from src.infrastructure.configs import DBConfig

engine = create_async_engine(
    DBConfig().DB_CONN_URL,
    pool_size=10,
    max_overflow=20,
)
SessionFactory = sessionmaker(bind=engine, class_=AsyncSession)


class IDBRepository(ABC):
    async def __aenter__(self) -> "IDBRepository":
        self.async_session: AsyncSession = SessionFactory()
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
