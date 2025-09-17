from pydantic import BaseModel
from datetime import datetime

class InventoryHistoryOut(BaseModel):
    id: int
    product_id: int
    change: int
    action: str
    updated_at: datetime

    class Config:
        from_attributes = True
