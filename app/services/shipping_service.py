from sqlalchemy.orm import Session
from app.models.shipping_model import Shipping
from app.schemas.shipping_schema import ShippingCreate
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status

def add_shipping(db: Session, shipping_data: ShippingCreate):
    shipping = Shipping(**shipping_data.dict())
    db.add(shipping)
    db.commit()
    db.refresh(shipping)
    return success_response(data=shipping, message="Shipping created successfully")

def get_shipping(db: Session, shipping_id: int):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise CustomException("Shipping not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=shipping, message="Shipping retrieved successfully")

def list_shipping(db: Session):
    shipping_records = db.query(Shipping).all()
    return success_response(data=shipping_records, message="Shipping records retrieved successfully")

def update_shipping(db: Session, shipping_id: int, update_data: dict):
    shipping = db.query(Shipping).filter(Shipping.id == shipping_id).first()
    if not shipping:
        raise CustomException("Shipping not found", status.HTTP_404_NOT_FOUND)

    for key, value in update_data.items():
        if value is not None:
            setattr(shipping, key, value)

    db.commit()
    db.refresh(shipping)
    return success_response(data=shipping, message="Shipping updated successfully")
