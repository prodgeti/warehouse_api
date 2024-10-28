from sqlalchemy.orm import Session
from models import Product, Order, OrderItem, OrderStatus
from schemas import ProductCreate, OrderCreate, OrderItemCreate
from fastapi import HTTPException
from datetime import date


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def update_product(db: Session, product_id: int, product_data: ProductCreate):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in product_data.dict().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}


def create_order(db: Session, order_data: OrderCreate):
    order = Order(created_date=date.today(), status=OrderStatus.in_progress)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_orders(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Order).offset(skip).limit(limit).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order


def create_order_item(db: Session, order_id: int, item_data: OrderItemCreate):
    product = get_product(db, item_data.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock_quantity < item_data.quantity:
        raise HTTPException(
            status_code=400, 
            detail="Insufficient product stock"
        )

    product.stock_quantity -= item_data.quantity
    db.commit()

    order_item = OrderItem(
        order_id=order_id,
        product_id=item_data.product_id,
        quantity=item_data.quantity
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item
