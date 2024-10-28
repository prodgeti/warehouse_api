from sqlalchemy import (Column, Integer,
                        String, Float,
                        ForeignKey, Date,
                        Enum, MetaData)
from sqlalchemy.orm import relationship, declarative_base

import enum

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class OrderStatus(str, enum.Enum):
    """Перечисление статусов заказа"""

    in_progress = "в процессе"
    shipped = "отправлен"
    delivered = "доставлен"


class Product(Base):
    """Модель товара"""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock_quantity = Column(Integer)


class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(Date)
    status = Column(Enum(OrderStatus), default=OrderStatus.in_progress)
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    """Модель элемента заказа"""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
