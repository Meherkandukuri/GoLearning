from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    unit = Column(String(32), nullable=False, default="kg")
    in_stock = Column(Boolean, default=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(120), nullable=True)
    customer_phone = Column(String(32), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(32), default="new")

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id"))
    product_name = Column(String(120), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(32), nullable=False)
    price_each = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")


