from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class ProductImageBase(BaseModel):
    image_url: str


class ProductImageCreate(ProductImageBase):
    pass


class ProductImageUpdate(BaseModel):
    image_url: Optional[str] = None


class ProductImageOut(ProductImageBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
