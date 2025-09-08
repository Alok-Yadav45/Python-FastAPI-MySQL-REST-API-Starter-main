from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class CategoryImageBase(BaseModel):
    image_url: str

class CategoryImageCreate(CategoryImageBase):
    pass

class CategoryImageUpdate(BaseModel):
    image_url: Optional[str] = None

class CategoryImageOut(CategoryImageBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True

class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
