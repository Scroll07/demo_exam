from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import func, ForeignKey, text
from datetime import datetime



class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    fio: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    
    orders: Mapped[list["Orders"]] = relationship(back_populates="user")
    
    
class Products(Base):
    __tablename__="products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    

class Orders(Base):
    __tablename__="orders"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(default=1)
    delivery_address: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str]

    user: Mapped["Users"] = relationship(back_populates="orders")






