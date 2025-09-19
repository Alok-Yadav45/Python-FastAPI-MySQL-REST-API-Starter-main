from pydantic import BaseModel
from datetime import datetime


class CartBase(BaseModel):
    product_id: int
    product_quantity: int


class CartCreate(CartBase):
    pass


class CartUpdate(BaseModel):
    product_quantity: int


class CartOut(CartBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
