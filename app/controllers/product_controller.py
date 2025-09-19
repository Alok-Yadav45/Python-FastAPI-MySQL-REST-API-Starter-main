from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas import product_schema, response_schema
from app.services import product_service
from app.helpers.response_helper import success_response
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.get("/", response_model=response_schema.ListResponse[product_schema.Product],
            dependencies=[Depends(role_checker("admin"))])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = product_service.get_products(db, skip=skip, limit=limit)
    return success_response(data=[product_schema.Product.from_orm(p) for p in products])


@router.get("/{product_id}", response_model=response_schema.SingleResponse[product_schema.Product])
def read_product(product_id: int, db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    product = product_service.get_product(db, product_id)
    return success_response(data=product_schema.Product.from_orm(product))


@router.post("/", response_model=response_schema.SingleResponse[product_schema.Product],
             dependencies=[Depends(role_checker("admin"))])
def create_product(product: product_schema.ProductCreate, db: Session = Depends(get_db)):
    new_product = product_service.create_product(db, product)
    return success_response(data=product_schema.Product.from_orm(new_product))


@router.put("/{product_id}", response_model=response_schema.SingleResponse[product_schema.Product])
def update_product(product_id: int, updates: product_schema.ProductUpdate,
                   db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    updated_product = product_service.update_product(db, product_id, updates)
    return success_response(data=product_schema.Product.from_orm(updated_product))


@router.delete("/{product_id}", response_model=response_schema.SingleResponse[product_schema.Product])
def delete_product(product_id: int, db: Session = Depends(get_db), current_user=Depends(verify_access_token)):
    deleted_product = product_service.delete_product(db, product_id)
    return success_response(data=product_schema.Product.from_orm(deleted_product))
