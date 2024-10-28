from pydantic import BaseModel
from datetime import date
from typing import List, Optional
import enum


class OrderStatus(str, enum.Enum):
    in_progress = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    created_date: date
    status: OrderStatus


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    items: List[OrderItem] = []

    class Config:
        orm_mode = True
