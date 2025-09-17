from pydantic import BaseModel
from datetime import datetime

class ProductInventoryCreate(BaseModel):
    product_id: int
    stock: int

class ProductInventoryOut(BaseModel):
    id: int
    product_id: int
    stock: int
    updated_at: datetime | None

    class Config:
        from_attributes = True