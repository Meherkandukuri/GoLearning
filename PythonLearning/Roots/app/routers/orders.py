from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db, engine
from .. import models, schemas


models.Base.metadata.create_all(bind=engine)


router = APIRouter()


@router.get("/", response_model=List[schemas.OrderRead])
def list_orders(db: Session = Depends(get_db)):
    orders = db.query(models.Order).order_by(models.Order.created_at.desc()).all()
    return orders


@router.post("/", response_model=schemas.OrderRead)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    order_obj = models.Order(customer_name=order.customer_name, customer_phone=order.customer_phone)
    db.add(order_obj)
    db.flush()

    for item in order.items:
        product_name = item.product_name
        unit = item.unit
        if item.product_id:
            product = db.query(models.Product).get(item.product_id)
            if product:
                product_name = product.name
                unit = product.unit

        oi = models.OrderItem(
            order_id=order_obj.id,
            product_id=item.product_id,
            product_name=product_name,
            quantity=item.quantity,
            unit=unit,
            price_each=item.price_each,
        )
        db.add(oi)

    db.commit()
    db.refresh(order_obj)
    return order_obj


