from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings

engine = create_async_engine(
    url=settings.POSTGRES_URL,
    # Log sql queries
    echo=True
)


async def create_db_tables():
    async with engine.begin() as connection:
        from app.api.schemas.shipment import Shipment  # noqa: F401
        await connection.run_sync(SQLModel.metadata.create_all(bind=engine))


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    with async_session() as session:
        yield session


# Session Dependency Annotation
SessionDep = Annotated[AsyncSession, Depends(get_session)]
