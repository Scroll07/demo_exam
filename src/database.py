from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio

from src.config import config
from src.dao.user_dao import UserDao
from src.models.models import Base
from src.dao.product_dao import ProductDao
from src.schemas import Register_DB, UserRoles
from src.services.secrets import create_hash

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
        
        try:
            await create_products(data=data)
            await create_admin()
        except Exception as e:
            print(f"Ошибка при инициализации бд: {e}")
        
        async_engine.echo = True
        
        
async def close_db():
    await async_engine.dispose()
    
    
async def create_products(data: list):
    async with async_session() as session:
        dao = ProductDao(session)
        for item in data:
            await dao.create_product(item)   
            
async def create_admin():
    password_hash = create_hash(config.ADMIN_PASSWORD)
    register_data = Register_DB(
        username=config.ADMIN_USERNAME,
        email="admin_email",
        password_hash=password_hash,
        fio="ADMIN",
        role=UserRoles.ADMIN,
        phone_number="admin_phone",
    )
    async with async_session() as session:
        dao = UserDao(session)
        await dao.register_user(register_data)     