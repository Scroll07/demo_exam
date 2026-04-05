from pydantic import BaseModel, Field
from enum import Enum



class RegisterRequest(BaseModel):
    username: str
    email: str 
    password: str = Field(min_length=4)
    fio: str
    phone_number: str


class Register_DB(BaseModel):
    username: str
    email: str 
    password_hash: str
    fio: str
    phone_number: str
    

class Product(BaseModel):
    id: int
    name: str
    price: int


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    DENIED = "denied"





