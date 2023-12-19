import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import config
from bot.database.models import Base

engine = create_async_engine(url=config.db.connection_db_string)
async_session_maker = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


async def delete_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


if __name__ == '__main__':
    asyncio.run(create_database())
