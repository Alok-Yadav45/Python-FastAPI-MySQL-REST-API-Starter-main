from sqlalchemy.orm import Session
from app.helpers import checkout_helper
from app.helpers.response_helper import success_response
from app.schemas.payment_schema import PaymentOut
from app.schemas.order_schema import OrderOut


def checkout(db: Session, user_id: int):
    order = checkout_helper.create_order_from_cart(db, user_id)
    return success_response(
        data=OrderOut.from_orm(order),
        message="Order created from cart successfully"
    )


def confirm_order(db: Session, order_id: int, user_id: int, method: str):
    order, payment = checkout_helper.confirm_order_with_payment(db, order_id, user_id, method)
    return success_response(
        data={
            "order": OrderOut.from_orm(order),
            "payment": PaymentOut.from_orm(payment)
        },
        message="Order confirmed and payment created"
    )
