from sqlalchemy.orm import Session
from fastapi import status
from ..helpers import category_helper
from ..schemas import category_schema
from ..helpers.exceptions import CustomException


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    return category_helper.get_categories(db, skip=skip, limit=limit)


def get_category(db: Session, category_id: int):
    category = category_helper.get_category(db, category_id)
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
    return category


def create_category(db: Session, category_data: category_schema.CategoryCreate):
    return category_helper.create_category(db, category_data)


def update_category(db: Session, category_id: int, updates: category_schema.CategoryUpdate):
    category = category_helper.get_category(db, category_id)
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
    return category_helper.update_category(db, category, updates)


def delete_category(db: Session, category_id: int):
    category = category_helper.get_category(db, category_id)
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
    return category_helper.delete_category(db, category)
