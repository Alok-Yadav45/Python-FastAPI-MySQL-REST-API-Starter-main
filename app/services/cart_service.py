from sqlalchemy.orm import Session
from app.helpers import cart_helper
from app.schemas.cart_schema import CartCreate, CartUpdate, CartOut
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status


def add_to_cart(db: Session, cart_data: CartCreate, user_id: int):
    cart_item = cart_helper.add_cart_item(db, cart_data, user_id)
    return success_response(
        data=CartOut.from_orm(cart_item),
        message="Product added to cart"
    )


def list_cart(db: Session, user_id: int):
    items = cart_helper.get_cart_items(db, user_id)
    return success_response(
        data=[CartOut.from_orm(item) for item in items],
        message="Cart retrieved successfully"
    )


def list_all_carts(db: Session):
    items = cart_helper.get_all_carts(db)
    return success_response(
        data=[CartOut.from_orm(item) for item in items],
        message="All carts retrieved successfully"
    )


def update_cart(db: Session, cart_id: int, update_data: CartUpdate):
    updated_item = cart_helper.update_cart_item(db, cart_id, update_data)
    return success_response(
        data=CartOut.from_orm(updated_item),
        message="Cart updated successfully"
    )


def remove_from_cart(db: Session, cart_id: int):
    removed_item = cart_helper.remove_cart_item(db, cart_id)
    return success_response(
        data=CartOut.from_orm(removed_item),
        message="Cart item removed successfully"
    )


def clear_cart(db: Session, user_id: int):
    cart_helper.clear_user_cart(db, user_id)
    return success_response(message="Cart cleared successfully")
