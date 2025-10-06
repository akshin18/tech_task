from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import AsyncSessionLocal


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
