from fastapi import status
from sqlalchemy.orm import Session
from app.helpers import category_helper
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut , APIResponse
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException


def create_category(db: Session, category_data: CategoryCreate):
    category = category_helper.create_category(db , category_data)
    return success_response(data=CategoryOut.from_orm(category), message="Category created successfully")

def get_category(db: Session, category_id: int):
    category = category_helper.get_category(db, category_id)
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=CategoryOut.from_orm(category), message="Category fetched successfully")

def get_all_categories(db: Session, skip: int = 0, limit: int = 100):
    categories = category_helper.get_all_categories(db, skip, limit)
    return success_response(data=[CategoryOut.from_orm(c) for c in categories],message="Categories fetched successfully")
                

def update_category(db: Session, category_id: int, updates: CategoryUpdate):   
    category = category_helper.get_category(db, category_id)    
    if not category:   
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)  
    updated = category_helper.update_category(db, category, updates) 
    return success_response(data=CategoryOut.from_orm(updated), message="Category updated successfully")   

def delete_category(db: Session, category_id: int): 
    category = category_helper.get_category(db, category_id)  
    if not category:  
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)  
    deleted = category_helper.delete_category(db, category)  
    return success_response(data=CategoryOut.from_orm(deleted), message="Category deleted successfully")      

   