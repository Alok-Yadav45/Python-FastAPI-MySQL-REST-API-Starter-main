from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewOut(ReviewBase):
    id: int
    user_id: int
    product_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
