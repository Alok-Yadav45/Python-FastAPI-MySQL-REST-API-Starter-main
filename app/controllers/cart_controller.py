from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.cart_schema import CartCreate, CartUpdate, CartOut
from app.schemas.media_schema import APIResponse
from app.services import cart_service

router = APIRouter()

@router.post("/carts", response_model=APIResponse[CartOut])
def add_to_cart(cart_data: CartCreate, db: Session = Depends(get_db)):
    return cart_service.add_to_cart(db, cart_data)


@router.get("/carts/{user_id}", response_model=APIResponse[List[CartOut]])
def list_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.list_cart(db, user_id)


@router.put("/carts/{cart_id}", response_model=APIResponse[CartOut])
def update_cart(cart_id: int, update_data: CartUpdate, db: Session = Depends(get_db)):
    return cart_service.update_cart(db, cart_id, update_data)


@router.delete("/carts/{cart_id}", response_model=APIResponse)
def remove_from_cart(cart_id: int, db: Session = Depends(get_db)):
    return cart_service.remove_from_cart(db, cart_id)


@router.delete("/carts/clear/{user_id}", response_model=APIResponse)
def clear_cart(user_id: int, db: Session = Depends(get_db)):
    return cart_service.clear_cart(db, user_id)
