from sqlalchemy.orm import Session
from fastapi import status
from app.helpers import product_helper
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse

from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException

def create_product(db: Session, product_data: ProductCreate):
    product = product_helper.create_product(db, product_data)
    if not product:
        raise CustomException(message="Invalid category_id", status_code=status.HTTP_400_BAD_REQUEST)
    return success_response(
        data=ProductResponse.from_orm(product), message="Product created successfully")

   
def get_product(db: Session, product_id: int):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)
    return success_response(
        data=ProductResponse.from_orm(product),
        message="Product fetched successfully"
    )

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    products = product_helper.get_all_products(db, skip, limit)
    return success_response(
    data=[ProductResponse.from_orm(p) for p in products],
    message="Products fetched successfully"
)


def update_product(db: Session, product_id: int, updates: ProductUpdate):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)
    
    updated = product_helper.update_product(db, product, updates)
    if not updated:
            raise CustomException(message="Invalid category_id", status_code=status.HTTP_400_BAD_REQUEST)
    return success_response(data=ProductResponse.from_orm(updated), message="Product updated successfully")


def delete_product(db: Session, product_id: int):
    product = product_helper.get_product(db, product_id)
    if not product:
        raise CustomException(message="Product not found", status_code=status.HTTP_404_NOT_FOUND)
    deleted = product_helper.delete_product(db, product)
    return success_response(data=ProductResponse.from_orm(deleted), message="Product deleted successfully")
    

