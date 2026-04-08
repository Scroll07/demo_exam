from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from src.schemas import Register_DB, VerifyData
from src.models.models import Users


class UserDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def register_user(self, user_data: Register_DB) -> None:
        try:
            new_user = Users(
                username=user_data.username,
                email=user_data.email,
                password_hash=user_data.password_hash,
                fio=user_data.fio,
                phone_number=user_data.phone_number
            )
            self.session.add(new_user)
            await self.session.commit()
        except Exception as e:
            await self.session.rollback()
            print(f'Ошибка при создании пользователя в бд: {e}')
            
    async def get_user_id_and_hash(self, username: str) -> VerifyData | None:
        query = (
            select(Users.id, Users.password_hash)
            .where(
                Users.username == username, 
            )
        )
        result = await self.session.execute(query)
        row = result.fetchone()
        if not row:
            return None
        return VerifyData(id=row[0], password_hash=row[1])
        
    