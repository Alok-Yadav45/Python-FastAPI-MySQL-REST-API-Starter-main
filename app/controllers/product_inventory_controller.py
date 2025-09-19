from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.product_inventory_schema import ProductInventoryCreate
from app.services import product_inventory_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.post("/", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def create_inventory(
    data: ProductInventoryCreate,
    db: Session = Depends(get_db)
):
    """Admin only: create inventory record for a product"""
    return product_inventory_service.create_inventory(db, data)


@router.post("/place-order/{product_id}/{quantity}", response_model=dict)
def place_order(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Reduce stock when order is placed (user or system)"""
    return product_inventory_service.place_order(db, product_id, quantity)


@router.post("/cancel-order/{product_id}/{quantity}", response_model=dict)
def cancel_order(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Increase stock when order is cancelled/returned"""
    return product_inventory_service.cancel_or_return_order(db, product_id, quantity)


@router.post("/restock/{product_id}/{quantity}", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def restock(
    product_id: int,
    quantity: int,
    db: Session = Depends(get_db)
):
    """Admin only: restock products"""
    return product_inventory_service.restock(db, product_id, quantity)


@router.get("/{product_id}", response_model=dict)
def get_inventory(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Any user can view stock availability"""
    return product_inventory_service.get_inventory(db, product_id)


@router.get("/history/{product_id}", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def get_inventory_history(
    product_id: int,
    db: Session = Depends(get_db)
):
    """Admin only: view history of stock changes"""
    return product_inventory_service.get_inventory_history(db, product_id)
