from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    price_at_purchase: float


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemOut(OrderItemBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    user_id: int
    status: Optional[str] = "pending"


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None


class OrderOut(OrderBase):
    id: int
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemOut] = []

    class Config:
        orm_mode = True
