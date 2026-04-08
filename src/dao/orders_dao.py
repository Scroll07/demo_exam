from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from sqlalchemy.orm import selectinload

from src.schemas import OrderStatus 
from src.models.models import Orders


class OrderDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create_order(
        self, 
        user_id: int, 
        product_id: int, 
        quantity: int,
        address: str
    ) -> Orders:
        status = OrderStatus.PENDING
        new_order = Orders(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            delivery_address=address,
            status=status
        )
        self.session.add(new_order)
        await self.session.commit()
        
        return new_order        
    
    async def get_user_orders(self, user_id: int) -> Sequence[Orders]:
        query = select(Orders).where(Orders.user_id == user_id).order_by(Orders.created_at.desc()).options(selectinload(Orders.product))
        result = await self.session.execute(query)
        orders = result.scalars().all()
        return orders
        
        
        
        
        
        
        