
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    currency: str = "INR"
    status: str = "pending"
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    user_id: int


class PaymentOut(PaymentBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
