from sqlalchemy.orm import Session
from fastapi import status
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product
from app.schemas.order_schema import OrderCreate, OrderUpdate
from app.helpers.exceptions import CustomException


def create_order(db: Session, order_data: OrderCreate, user_id: int):
    order = Order(user_id=user_id, status="pending")
    total = 0

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise CustomException(
                message=f"Product {item.product_id} not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        line_total = item.product_quantity * product.price
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
    return order


def get_order(db: Session, order_id: int, user_id: int):
    return db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()


def get_orders_by_user(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def get_all_orders(db: Session):
    return db.query(Order).all()


def update_order(db: Session, order: Order, update_data: OrderUpdate):
    if update_data.status is not None:
        order.status = update_data.status
    if update_data.payment_id is not None:
        order.payment_id = update_data.payment_id

    db.commit()
    db.refresh(order)
    return order


def delete_order(db: Session, order: Order):
    db.delete(order)
    db.commit()
    return order
