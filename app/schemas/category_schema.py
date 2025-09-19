from pydantic import BaseModel, Field
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    parent_id: Optional[int] = None


class Category(CategoryBase):
    id: int
    children: List["Category"] = Field(default_factory=list)  

    class Config:
        from_attributes = True



Category.model_rebuild()
