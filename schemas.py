from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class OrderBase(BaseModel):
    created_date: date
    status: OrderStatus


class OrderCreate(OrderBase):
    status: OrderStatus = OrderStatus.in_progress
    items: List[OrderItemCreate] = []


class Order(OrderBase):
    id: int
    items: List[OrderItem] = []

    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
