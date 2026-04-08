from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio


from src.models.models import Base
from src.dao.product_dao import ProductDao

async_engine = create_async_engine("sqlite+aiosqlite:///./avoska.db")

async_session = async_sessionmaker(async_engine, expire_on_commit=False)
    
data = [
    {"name": "Bucket", "price": 10},
    {"name": "Iron", "price": 4},
    {"name": "Shovel", "price": 6},
    {"name": "Shield", "price": 12},
    {"name": "Tower", "price": 100},
]

async def init_db():
    async with async_engine.begin() as conn:
        async_engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        await create_products(data=data)
        
        async_engine.echo = True
        
        
async def close_db():
    await async_engine.dispose()
    
    
async def create_products(data: list):
    async with async_session() as session:
        dao = ProductDao(session)
        for item in data:
            await dao.create_product(item)        