from pydantic import BaseModel, Field
from typing import Optional, List, TypeVar, Generic

T = TypeVar("T")


class MediaBase(BaseModel):
    file_url: str
    file_type: str
    filename: str


class MediaCreate(MediaBase):
    product_id: Optional[int] = None
    category_id: Optional[int] = None


class MediaUpdate(BaseModel):
    file_url: Optional[str] = None
    file_type: Optional[str] = None
    filename: Optional[str] = None


class Media(MediaBase):
    id: int
    product_id: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True
