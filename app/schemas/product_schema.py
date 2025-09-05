from pydantic import BaseModel
from typing import Optional, Union

class ProductBase(BaseModel):
    sku: str
    name: str
    description: str
    price: float
    stock: int
    category_id: int

class ProductCreate(ProductBase):
    pass 

class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    stock: int | None = None
    category_id: int | None = None 

class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True 

class ProductResponse(BaseModel):
    sku: str
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: int


    class Config:
        from_attributes = True

class APIResponse(BaseModel):
    success: bool
    message: str
    data: Union[ProductResponse, list[ProductResponse]]