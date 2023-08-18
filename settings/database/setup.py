from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from data.config import connection_db_string


async def create_db_session():
    engine = create_async_engine(url=connection_db_string)

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    return async_session
