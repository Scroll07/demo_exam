from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.models.models import Base


async_engine = create_async_engine("sqlite+aiosqlite:///./avoska.db")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)

async def init_db():
    async with async_engine.begin() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        async_engine.echo = True
        
        
async def close_db():
    await async_engine.dispose()