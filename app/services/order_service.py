from sqlalchemy.orm import Session
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status


def add_order(db: Session, order_data: OrderCreate, user_id: int):
    order = Order(user_id=user_id, status=order_data.status or "pending")

    total = 0
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise CustomException(f"Product {item.product_id} not found", status.HTTP_404_NOT_FOUND)

        line_total = item.product_quantity * item.product_price
        total += line_total
        order.items.append(
            OrderItem(
                product_id=item.product_id,
                product_price=product.price,
                product_quantity=item.product_quantity,
                total_price=line_total,
            )
        )

    order.total_amount = total
    db.add(order)
    db.commit()
    db.refresh(order)

    return success_response(data=order, message="Order created successfully")


def get_order(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=order, message="Order retrieved successfully")


def list_orders(db: Session, user_id: int):
    orders = db.query(Order).filter(Order.user_id == user_id).all()
    return success_response(data=orders, message="Orders retrieved successfully")


def update_order(db: Session, order_id: int, update_data: OrderUpdate, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    if update_data.status is not None:
        order.status = update_data.status
    if update_data.payment_id is not None:
        order.payment_id = update_data.payment_id

    db.commit()
    db.refresh(order)
    return success_response(data=order, message="Order updated successfully")
