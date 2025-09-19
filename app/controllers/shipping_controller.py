from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.shipping_schema import ShippingCreate, ShippingOut
from app.services import shipping_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.post("/", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def add_shipping(
    shipping_data: ShippingCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: create shipping record for an order"""
    return shipping_service.add_shipping(db, shipping_data)


@router.get("/{shipping_id}", response_model=dict)
def get_shipping(
    shipping_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """
    Users: can only access their own shipping (linked to their orders).  
    Admins: can access any shipping.
    """
    return shipping_service.get_shipping(db, shipping_id, token_data)


@router.get("/", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def list_shipping(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: list all shipping records"""
    return shipping_service.list_shipping(db)


@router.put("/{shipping_id}", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def update_shipping(
    shipping_id: int,
    update_data: dict,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: update shipping record"""
    return shipping_service.update_shipping(db, shipping_id, update_data)
