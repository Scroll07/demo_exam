from datetime import datetime

from pydantic import BaseModel, Field
from enum import Enum, StrEnum



class RegisterRequest(BaseModel):
    username: str
    email: str 
    password: str = Field(min_length=4)
    fio: str
    role: "UserRoles"
    phone_number: str


class Register_DB(BaseModel):
    username: str
    email: str 
    password_hash: str
    fio: str
    role: "UserRoles"
    phone_number: str


class OrderResponse(BaseModel):
    product_name: str
    quantity: int
    address: str
    status: "OrderStatus"
    created_at: datetime
    
    

class Product(BaseModel):
    id: int
    name: str
    price: int

    
class VerifyData(BaseModel):
    id: int
    password_hash: str



class UserValidateData(BaseModel):
    user_id: int
    role: "UserRoles"

class UserRoles(StrEnum):
    USER = "user"
    ADMIN = "admin"


class OrderStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DENIED = "denied"

