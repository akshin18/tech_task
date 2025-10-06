import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.db.session import get_db
from app.main import app


@pytest.fixture(scope="session")
def event_loop():

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    # Create a test database engine
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Close the engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def override_get_db(db_engine):
    # Create a new session for each test
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async def _get_db():
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.rollback()

    # Override the get_db dependency
    app.dependency_overrides[get_db] = _get_db
    yield
    # Clean up the override after the test
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def session(override_get_db, db_engine):
    # Create a session that can be used in tests that need direct access to the db session
    async_session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


@pytest.fixture(scope="function")
def client():
    from fastapi.testclient import TestClient
    from app.db.session import get_db
    from sqlalchemy.ext.asyncio import create_async_engine
    from sqlalchemy.orm import sessionmaker
    from app.db.base import Base

    # Create an in-memory database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    # Create all tables
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_tables())

    # Create async session
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Define the override function
    async def override_get_db():
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.rollback()  # Use rollback instead of close for testing

    # Apply the override
    app.dependency_overrides[get_db] = override_get_db

    # Create the test client
    with TestClient(app) as test_client:
        yield test_client

    # Clean up the override after the test
    app.dependency_overrides.clear()
