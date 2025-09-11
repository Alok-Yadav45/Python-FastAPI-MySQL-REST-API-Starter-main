from sqlalchemy.orm import Session
from app.models.order_model import Order, OrderItem
from app.schemas.order_schema import OrderCreate, OrderUpdate, OrderItemCreate
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status


def add_order(db: Session, order_data: OrderCreate):
    order = Order(user_id=order_data.user_id, status=order_data.status or "pending")

    total = 0
    for item in order_data.items:
        line_total = item.product_quantity * item.product_price
        total += line_total
        order.items.append(
            OrderItem(
                product_id=item.product_id,
                product_quantity=item.product_quantity,
                total_price=line_total,
            )
        )

    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)

    return success_response(data=order, message="Order created successfully")


def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=order, message="Order retrieved successfully")


def list_orders(db: Session):
    orders = db.query(Order).all()
    return success_response(data=orders, message="Orders retrieved successfully")


def update_order(db: Session, order_id: int, update_data: OrderUpdate):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    if update_data.status is not None:
        order.status = update_data.status

    db.commit()
    db.refresh(order)
    return success_response(data=order, message="Order updated successfully")

