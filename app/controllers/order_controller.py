from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.order_schema import OrderCreate, OrderOut, OrderUpdate
from app.schemas import user_schema
from app.schemas.media_schema import APIResponse
from app.services import order_service
from app.middleware.verify_access_token import verify_access_token  

router = APIRouter()

@router.post("/orders", response_model=APIResponse[OrderOut])
def add_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(verify_access_token)
):
    return order_service.add_order(db, order_data, current_user)


@router.get("/orders/{order_id}", response_model=APIResponse[OrderOut])
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return order_service.get_order(db, order_id, user_id)


@router.get("/orders", response_model=APIResponse[List[OrderOut]])
def list_orders(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return order_service.list_orders(db, user_id)


@router.put("/orders/{order_id}", response_model=APIResponse[OrderOut])
def update_order(
    order_id: int,
    update_data: OrderUpdate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return order_service.update_order(db, order_id, update_data, user_id)
