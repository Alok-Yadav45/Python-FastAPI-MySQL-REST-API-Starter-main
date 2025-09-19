from sqlalchemy.orm import Session
from app.helpers import shipping_helper
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from app.schemas.shipping_schema import ShippingOut


def add_shipping(db: Session, shipping_data):
    shipping = shipping_helper.create_shipping(db, shipping_data)
    return success_response(
        data=ShippingOut.from_orm(shipping),
        message="Shipping created successfully"
    )


def get_shipping(db: Session, shipping_id: int, token_data: dict):
    shipping = shipping_helper.get_shipping_by_id(db, shipping_id)

    if token_data["role"] != "admin":
        if shipping.order.user_id != token_data["user_id"]:
            raise CustomException("Not authorized to view this shipping record", 403)

    return success_response(
        data=ShippingOut.from_orm(shipping),
        message="Shipping retrieved successfully"
    )


def list_shipping(db: Session):
    records = shipping_helper.get_all_shipping(db)
    return success_response(
        data=[ShippingOut.from_orm(record) for record in records],
        message="Shipping records retrieved successfully"
    )


def update_shipping(db: Session, shipping_id: int, update_data: dict):
    shipping = shipping_helper.update_shipping(db, shipping_id, update_data)
    return success_response(
        data=ShippingOut.from_orm(shipping),
        message="Shipping updated successfully"
    )
