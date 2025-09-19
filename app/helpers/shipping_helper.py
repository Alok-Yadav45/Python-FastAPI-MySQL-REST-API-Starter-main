from sqlalchemy.orm import Session
from app.models.shipping_model import Shipping
from app.schemas.shipping_schema import ShippingCreate
from app.helpers.exceptions import CustomException
from fastapi import status


def create_shipping(db: Session, shipping_data: ShippingCreate) -> Shipping:
    shipping = Shipping(**shipping_data.dict())
    db.add(shipping)
    db.commit()
    db.refresh(shipping)
    return shipping


def get_shipping_by_id(db: Session, shipping_id: int) -> Shipping:
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise CustomException("Shipping not found", status.HTTP_404_NOT_FOUND)
    return shipping


def get_all_shipping(db: Session):
    return db.query(Shipping).all()


def update_shipping(db: Session, shipping_id: int, update_data: dict) -> Shipping:
    shipping = get_shipping_by_id(db, shipping_id)

    for key, value in update_data.items():
        if value is not None:
            setattr(shipping, key, value)

    db.commit()
    db.refresh(shipping)
    return shipping
