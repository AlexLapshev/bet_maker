from abc import ABC, abstractmethod
from typing import Optional, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import PostgresSettings


class Database(ABC):
    def __init__(self) -> None:
        self.async_sessionmaker: Optional[sessionmaker] = None

    async def __call__(self) -> AsyncIterator[AsyncSession]:
        if not self.async_sessionmaker:
            raise ValueError(
                "async_sessionmaker not available. Run setup() first."
            )  # noqa
        async with self.async_sessionmaker() as session:
            async with session.begin():
                yield session

    @abstractmethod
    def setup(self) -> None:
        raise NotImplementedError


def get_connection_string(driver: str = "asyncpg") -> str:
    if driver:
        driver = f"+{driver}"
    return (
        f"postgresql{driver}://"
        f"{PostgresSettings.POSTGRES_USERNAME}:"
        f"{PostgresSettings.POSTGRES_PASSWORD}@"
        f"{PostgresSettings.POSTGRES_HOST}:"
        f"{PostgresSettings.POSTGRES_PORT}/"
        f"{PostgresSettings.POSTGRES_DB_NAME}"
    )


class PostgresDatabase(Database):
    def setup(self, echo: Optional[bool] = None) -> None:
        async_engine = create_async_engine(
            get_connection_string(),
            echo=echo,
        )
        self.async_sessionmaker = sessionmaker(  # type: ignore
            bind=async_engine, class_=AsyncSession
        )


db = PostgresDatabase()  # type: ignore
Base = declarative_base()
