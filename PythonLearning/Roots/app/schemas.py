from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    unit: str = Field(default="kg")
    in_stock: bool = True


class ProductRead(ProductCreate):
    id: int

    class Config:
        orm_mode = True


class OrderItemCreate(BaseModel):
    product_id: Optional[int] = None
    product_name: str
    quantity: float
    unit: str
    price_each: float


class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    items: List[OrderItemCreate]


class OrderItemRead(OrderItemCreate):
    id: int

    class Config:
        orm_mode = True


class OrderRead(BaseModel):
    id: int
    customer_name: Optional[str]
    customer_phone: Optional[str]
    created_at: datetime
    status: str
    items: List[OrderItemRead]

    class Config:
        orm_mode = True


