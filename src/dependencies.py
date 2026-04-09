from fastapi import Request, HTTPException

from src.database import async_session
from src.schemas import UserValidateData



async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            
async def user_validate(request: Request) -> UserValidateData:
    user_id = request.session.get("user_id")
    role = request.session.get("role")
    if not role or not user_id:
        raise HTTPException(403, detail="Unauthorized")
    return UserValidateData(user_id=user_id, role=role)