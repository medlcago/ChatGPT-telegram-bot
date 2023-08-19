from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


async def create_db_session(url: str):
    engine = create_async_engine(url=url)

    async_session = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)
    return async_session
