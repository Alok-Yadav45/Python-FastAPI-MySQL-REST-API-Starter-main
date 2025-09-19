from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from app.services import order_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker
from app.schemas.response_schema import SingleResponse, ListResponse


router = APIRouter()


@router.post("/", response_model=SingleResponse[OrderOut])
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return order_service.add_order(db, order_data, token_data["user_id"])


@router.get("/{order_id}", response_model=SingleResponse[OrderOut])
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return order_service.get_order(db, order_id, token_data["user_id"])


@router.get("/", response_model=ListResponse[OrderOut])
def list_orders(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return order_service.list_orders(db, token_data["user_id"])


@router.get("/all", response_model=ListResponse[OrderOut], dependencies=[Depends(role_checker(["admin"]))])
def list_all_orders(db: Session = Depends(get_db)):
    """Admin only"""
    return order_service.list_all_orders(db)


@router.put("/{order_id}", response_model=SingleResponse[OrderOut])
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return order_service.update_order(db, order_id, update_data, token_data["user_id"])


@router.delete("/{order_id}", response_model=SingleResponse[OrderOut], dependencies=[Depends(role_checker(["admin"]))])
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    return order_service.delete_order(db, order_id)
