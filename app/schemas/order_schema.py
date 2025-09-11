from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    product_quantity: int
    product_price: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int
    total_price: float

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    status: Optional[str] = "pending"
    payment_id: Optional[str] = None


class OrderCreate(OrderBase):
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
        orm_mode = True
