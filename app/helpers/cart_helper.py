from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.schemas.cart_schema import CartCreate, CartUpdate
from app.helpers.exceptions import CustomException
from fastapi import status


def add_cart_item(db: Session, cart_data: CartCreate, user_id: int):
    """Add a product to cart or increase its quantity if already exists."""
    cart_item = db.query(Cart).filter(
        Cart.user_id == user_id,
        Cart.product_id == cart_data.product_id
    ).first()

    if cart_item:
        cart_item.product_quantity += cart_data.product_quantity
    else:
        cart_item = Cart(
            user_id=user_id,
            product_id=cart_data.product_id,
            product_quantity=cart_data.product_quantity,
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_cart_items(db: Session, user_id: int):
    return db.query(Cart).filter(Cart.user_id == user_id).all()


def get_all_carts(db: Session):
    """Admin: fetch all carts"""
    return db.query(Cart).all()


def get_cart_item(db: Session, cart_id: int):
    return db.query(Cart).filter(Cart.id == cart_id).first()


def update_cart_item(db: Session, cart_id: int, update_data: CartUpdate):
    cart_item = get_cart_item(db, cart_id)
    if not cart_item:
        raise CustomException("Cart item not found", status.HTTP_404_NOT_FOUND)

    cart_item.product_quantity = update_data.product_quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def remove_cart_item(db: Session, cart_id: int):
    cart_item = get_cart_item(db, cart_id)
    if not cart_item:
        raise CustomException("Cart item not found", status.HTTP_404_NOT_FOUND)

    db.delete(cart_item)
    db.commit()
    return cart_item


def clear_user_cart(db: Session, user_id: int):
    db.query(Cart).filter(Cart.user_id == user_id).delete()
    db.commit()
