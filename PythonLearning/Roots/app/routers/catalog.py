from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db, Base, engine
from .. import models, schemas


# Ensure tables exist (simple auto-migrate for demo)
models.Base.metadata.create_all(bind=engine)


router = APIRouter()


@router.get("/", response_model=List[schemas.ProductRead])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()


@router.post("/", response_model=schemas.ProductRead)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    exists = db.query(models.Product).filter(models.Product.name == product.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Product already exists")
    obj = models.Product(**product.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/{product_id}", response_model=schemas.ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    return obj


@router.put("/{product_id}", response_model=schemas.ProductRead)
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    for k, v in data.dict().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Product).get(product_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(obj)
    db.commit()
    return {"ok": True}


