
from fastapi import HTTPException

from src.dao.user_dao import UserDao
from src.schemas import VerifyData
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.secrets import verify_hash


async def authorize(session: AsyncSession, username: str, password: str) -> int:
    dao = UserDao(session)
    data = await dao.get_user_id_and_hash(username)
    if not data:
        raise HTTPException(401, "Непривильный логин или пароль")

    if not verify_hash(password, data.password_hash):
        raise HTTPException(401, "Непривильный логин или пароль")   
    
    return data.id