from fastapi import status
from sqlalchemy.orm import Session
from app.helpers import category_helper
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, Categoryout, APIResponse
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException


def create_category(db: Session, category_data: CategoryCreate):
    category = category_helper.create_category(db , category_data)
    return success_response(data=Categoryout.from_orm(category), message="Category created successfully")

def get_category(db: Session, category_id: int):
    category = category_helper.get_category(db, category_id)
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=Categoryout.from_orm(category), message="Category fetched successfully")
