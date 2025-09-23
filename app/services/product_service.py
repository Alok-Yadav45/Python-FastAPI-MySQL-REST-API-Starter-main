from sqlalchemy.orm import Session
from typing import Optional
from fastapi import status
from ..helpers import product_helper
from ..schemas import product_schema
from ..helpers.exceptions import CustomException


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return product_helper.get_products(db, skip, limit)


def get_product(db: Session, product_id: int):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException("Product not found", status.HTTP_404_NOT_FOUND)
    return product


def create_product(db: Session, product_data: product_schema.ProductCreate):
    product = product_helper.create_product(db, product_data)
    if not product:
        raise CustomException("Invalid category_id", status.HTTP_400_BAD_REQUEST)
    return product


def update_product(db: Session, product_id: int, updates: product_schema.ProductUpdate):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException("Product not found", status.HTTP_404_NOT_FOUND)

    updated = product_helper.update_product(db, product, updates)
    if not updated:
        raise CustomException("Invalid category_id", status.HTTP_400_BAD_REQUEST)
    return updated


def delete_product(db: Session, product_id: int):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException("Product not found", status.HTTP_404_NOT_FOUND)
    return product_helper.delete_product(db, product)

def search_products(db: Session, query_text: str, skip: int = 0, limit: int = 100):
    return product_helper.search_products(db=db, query_text=query_text, skip=skip, limit=limit)


def filter_products(
    db: Session,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
):
    return product_helper.filter_products(
        db=db,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price,
        in_stock=in_stock,
        skip=skip,
        limit=limit
    )