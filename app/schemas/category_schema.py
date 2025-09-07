from pydantic import BaseModel
from typing import Optional, List

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass 

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    parent_id: Optional[int] = None

class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    success: bool
    message: str
    data: CategoryOut | list[CategoryOut]