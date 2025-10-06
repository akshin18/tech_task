import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.db.base import Base
from app.core.config import settings


async def init_db():
    """
    Initialize the database by creating all tables.
    """
    print("Creating database tables...")
    temp_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    async with temp_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await temp_engine.dispose()
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())
