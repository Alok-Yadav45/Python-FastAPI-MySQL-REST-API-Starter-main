from sqlalchemy.orm import Session
from fastapi import status
from app.helpers import order_helper
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderOut
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from app.models.order_model import Order


def add_order(db: Session, order_data: OrderCreate, user_id: int):
    order = order_helper.create_order(db, order_data, user_id)
    return success_response(
        data=OrderOut.from_orm(order),
        message="Order created successfully"
    )


def get_order(db: Session, order_id: int, user_id: int):
    order = order_helper.get_order(db, order_id, user_id)
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)
    return success_response(
        data=OrderOut.from_orm(order),
        message="Order retrieved successfully"
    )


def list_orders(db: Session, user_id: int):
    orders = order_helper.get_orders_by_user(db, user_id)
    return success_response(
        data=[OrderOut.from_orm(o) for o in orders],
        message="Orders retrieved successfully"
    )


def list_all_orders(db: Session):
    orders = order_helper.get_all_orders(db)
    return success_response(
        data=[OrderOut.from_orm(o) for o in orders],
        message="All orders retrieved successfully"
    )


def update_order(db: Session, order_id: int, update_data: OrderUpdate, user_id: int):
    order = order_helper.get_order(db, order_id, user_id)
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    updated = order_helper.update_order(db, order, update_data)
    return success_response(
        data=OrderOut.from_orm(updated),
        message="Order updated successfully"
    )


def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    deleted = order_helper.delete_order(db, order)
    return success_response(
        data=OrderOut.from_orm(deleted),
        message="Order deleted successfully"
    )
