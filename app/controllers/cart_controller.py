from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.cart_schema import CartCreate, CartUpdate, CartOut
from app.schemas.response_schema import SingleResponse, ListResponse 
from app.services import cart_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/", response_model=SingleResponse[CartOut])
def add_to_cart(
    cart_data: CartCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return cart_service.add_to_cart(db, cart_data, token_data["user_id"])


@router.get("/", response_model=ListResponse[CartOut])
def list_cart(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return cart_service.list_cart(db, token_data["user_id"])


@router.get(
    "/all",
    response_model=ListResponse[CartOut],
    dependencies=[Depends(role_checker(["admin"]))]
)
def list_all_carts(
    db: Session = Depends(get_db)
):
    """Admin only: list all carts"""
    return cart_service.list_all_carts(db)


@router.put("/{cart_id}", response_model=SingleResponse[CartOut])
def update_cart(
    cart_id: int,
    update_data: CartUpdate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return cart_service.update_cart(db, cart_id, update_data)


@router.delete("/{cart_id}", response_model=SingleResponse[CartOut])
def remove_from_cart(
    cart_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return cart_service.remove_from_cart(db, cart_id)


@router.delete("/clear", response_model=SingleResponse[dict])
def clear_cart(
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    return cart_service.clear_cart(db, token_data["user_id"])
