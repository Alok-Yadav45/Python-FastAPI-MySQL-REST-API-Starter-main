from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class OrderItemBase(BaseModel):
    product_id: int
    product_quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int
    product_price: float
    total_price: float

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    status: Optional[str] = "pending"
    payment_id: Optional[str] = None


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_id: Optional[str] = None


class OrderOut(OrderBase):
    id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        from_attributes = True
