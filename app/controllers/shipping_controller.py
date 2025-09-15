# app/controllers/shipping_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.shipping_schema import ShippingCreate, ShippingOut
from app.schemas.media_schema import APIResponse
from app.services import shipping_service
from app.middleware.verify_access_token import verify_access_token  

router = APIRouter()

@router.post("/shipping", response_model=APIResponse[ShippingOut])
def add_shipping(
    shipping_data: ShippingCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return shipping_service.add_shipping(db, shipping_data)

@router.get("/shipping/{shipping_id}", response_model=APIResponse[ShippingOut])
def get_shipping(shipping_id: int, db: Session = Depends(get_db)):
    return shipping_service.get_shipping(db, shipping_id)

@router.get("/shipping", response_model=APIResponse[List[ShippingOut]])
def list_shipping(db: Session = Depends(get_db)):
    return shipping_service.list_shipping(db)

@router.put("/shipping/{shipping_id}", response_model=APIResponse[ShippingOut])
def update_shipping(
    shipping_id: int,
    update_data: dict,
    db: Session = Depends(get_db)
):
    return shipping_service.update_shipping(db, shipping_id, update_data)
