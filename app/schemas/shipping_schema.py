from pydantic import BaseModel
from typing import Optional

class ShippingBase(BaseModel):
    address: str
    courier: str
    tracking_number: Optional[str] = None
    status: Optional[str] = "preparing"

class ShippingCreate(ShippingBase):
    order_id: int

class ShippingOut(ShippingBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True
