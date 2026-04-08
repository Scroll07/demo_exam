from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence

from src.models.models import Products 

class ProductDao:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
        
    async def create_product(self, data: dict) -> Products:
        new_product = Products(
            name=data["name"],
            price=data["price"]
        )
        self.session.add(new_product)
        await self.session.commit()
        await self.session.refresh(new_product)
        return new_product
    
    async def get_products(self) -> Sequence[Products]:
        query = select(Products)
        result = await self.session.execute(query)
        products = result.scalars().all()
        return products