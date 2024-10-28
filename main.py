from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import (
    create_product, get_products, get_product, update_product, delete_product,
    create_order, get_orders, get_order, update_order_status, create_order_item
)
from schemas import (Product, ProductCreate,
                     Order, OrderCreate,
                     OrderItemCreate, OrderStatus)

app = FastAPI()


@app.post("/products", response_model=Product)
def create_product_endpoint(
    product: ProductCreate,
    db: Session = Depends(get_db)
):
    return create_product(db, product)


@app.get("/products", response_model=list[Product])
def get_products_endpoint(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_products(db, skip=skip, limit=limit)


@app.get("/products/{product_id}", response_model=Product)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@app.put("/products/{product_id}", response_model=Product)
def update_product_endpoint(
    product_id: int,
    product_data: ProductCreate,
    db: Session = Depends(get_db)
):
    return update_product(db, product_id, product_data)


@app.delete("/products/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    return delete_product(db, product_id)


@app.post("/orders", response_model=Order)
def create_order_endpoint(
    order_data: OrderCreate, 
    db: Session = Depends(get_db)
):
    return create_order(db, order_data)


@app.get("/orders", response_model=list[Order])
def get_orders_endpoint(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_orders(db, skip=skip, limit=limit)


@app.get("/orders/{order_id}", response_model=Order)
def get_order_endpoint(order_id: int, db: Session = Depends(get_db)):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status_endpoint(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db)
):
    return update_order_status(db, order_id, status)


@app.post("/orders/{order_id}/items", response_model=Order)
def add_order_item(
    order_id: int,
    item_data: OrderItemCreate,
    db: Session = Depends(get_db)
):
    order = get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    create_order_item(db, order_id, item_data)
    db.refresh(order)
    return order
