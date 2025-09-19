from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas import category_schema, response_schema
from app.services import category_service
from app.helpers.response_helper import success_response
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.get("/", response_model=response_schema.ListResponse[category_schema.Category],
            dependencies=[Depends(role_checker("admin"))])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    categories = category_service.get_categories(db, skip=skip, limit=limit)
    return success_response(data=[category_schema.Category.from_orm(c) for c in categories])


@router.get("/{category_id}", response_model=response_schema.SingleResponse[category_schema.Category])
def read_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    category = category_service.get_category(db, category_id)
    return success_response(data=category_schema.Category.from_orm(category))


@router.post("/", response_model=response_schema.SingleResponse[category_schema.Category],
             dependencies=[Depends(role_checker("admin"))])
def create_category(category: category_schema.CategoryCreate, db: Session = Depends(get_db)):
    new_category = category_service.create_category(db, category)
    return success_response(data=category_schema.Category.from_orm(new_category))


@router.put("/{category_id}", response_model=response_schema.SingleResponse[category_schema.Category])
def update_category(category_id: int, updates: category_schema.CategoryUpdate,
                    db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    updated_category = category_service.update_category(db, category_id, updates)
    return success_response(data=category_schema.Category.from_orm(updated_category))


@router.delete("/{category_id}", response_model=response_schema.SingleResponse[category_schema.Category])
def delete_category(category_id: int, db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    deleted_category = category_service.delete_category(db, category_id)
    return success_response(data=category_schema.Category.from_orm(deleted_category))
