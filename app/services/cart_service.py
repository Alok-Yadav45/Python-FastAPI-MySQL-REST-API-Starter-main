from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status


def add_to_cart(db: Session, cart_data):
    cart_item = db.query(Cart).filter(
        Cart.user_id == cart_data.user_id,
        Cart.product_id == cart_data.product_id
    ).first()

    if cart_item:
        cart_item.product_quantity += cart_data.product_quantity
    else:
        cart_item = Cart(
            user_id=cart_data.user_id,
            product_id=cart_data.product_id,
            product_quantity=cart_data.product_quantity,
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return success_response(data=cart_item, message="Product added to cart")


def list_cart(db: Session, user_id: int):
    items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return success_response(data=items, message="Cart retrieved successfully")


def update_cart(db: Session, cart_id: int, update_data):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise CustomException("Cart item not found", status.HTTP_404_NOT_FOUND)

    cart_item.product_quantity = update_data.product_quantity
    db.commit()
    db.refresh(cart_item)
    return success_response(data=cart_item, message="Cart updated successfully")


def remove_from_cart(db: Session, cart_id: int):
    cart_item = db.query(Cart).filter(Cart.id == cart_id).first()
    if not cart_item:
        raise CustomException("Cart item not found", status.HTTP_404_NOT_FOUND)

    db.delete(cart_item)
    db.commit()
    return success_response(message="Cart item removed successfully")


def clear_cart(db: Session, user_id: int):
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
    return success_response(message="Cart cleared successfully")

