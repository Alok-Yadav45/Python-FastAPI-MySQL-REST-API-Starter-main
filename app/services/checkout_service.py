
from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.models.order_model import Order, OrderItem
from app.models.payment_model import Payment
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status

def checkout(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise CustomException("Cart is empty", status.HTTP_400_BAD_REQUEST)

    order = Order(user_id=user_id, status="pending")
    total_amount = 0

    for cart in cart_items:
        line_total = cart.product_quantity * 100  
        total_amount += line_total

        order.items.append(
            OrderItem(
                product_id=cart.product_id,
                product_price=100, 
                product_quantity=cart.product_quantity,
                total_price=line_total,
            )
        )
    
    for cart in cart_items:
        db.delete(cart)

    db.commit()
    db.refresh(order)

    return success_response(data=order, message="Order created from cart successfully")


def confirm_order(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    order.status = "confirmed"

    payment = Payment(
        user_id=user_id,
        order_id=order.id,
        amount=order.total_amount,
        currency="INR",
        status="pending",
    )
    db.add(payment)

    db.commit()
    db.refresh(order)
    db.refresh(payment)

    return success_response(data={"order": order, "payment": payment}, message="Order confirmed and payment created")

