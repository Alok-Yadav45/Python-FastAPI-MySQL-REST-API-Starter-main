
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    currency: str = "INR"
    method: str


class PaymentCreate(PaymentBase):
    pass


class PaymentOut(PaymentBase):
    id: int
    status: str               
    transaction_id: str | None
    created_at: datetime
    updated_at: datetime
  

    class Config:
        from_attributes = True
