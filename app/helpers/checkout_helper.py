from sqlalchemy.orm import Session
from app.models.cart_model import Cart
from app.models.order_model import Order, OrderItem
from app.models.payment_model import Payment
from app.models.product_model import Product
from app.helpers.exceptions import CustomException
from fastapi import status


def create_order_from_cart(db: Session, user_id: int) -> Order:
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    if not cart_items:
        raise CustomException("Cart is empty", status.HTTP_400_BAD_REQUEST)

    order = Order(user_id=user_id, status="pending")
    total_amount = 0

    for cart in cart_items:
        product = db.query(Product).filter(Product.id == cart.product_id).first()
        if not product:
            raise CustomException(
                f"Product with ID {cart.product_id} not found",
                status.HTTP_404_NOT_FOUND
            )

        if product.stock < cart.product_quantity:
            raise CustomException(
                f"Not enough stock for product {product.name}. "
                f"Available: {product.stock}, Requested: {cart.product_quantity}",
                status.HTTP_400_BAD_REQUEST
            )

        line_total = cart.product_quantity * product.price
        total_amount += line_total

        order.items.append(
            OrderItem(
                product_id=cart.product_id,
                product_price=product.price,
                product_quantity=cart.product_quantity,
                total_price=line_total,
            )
        )

        product.stock -= cart.product_quantity

    order.total_amount = total_amount
    db.add(order)

    # clear cart after creating order
    for cart in cart_items:
        db.delete(cart)

    db.commit()
    db.refresh(order)
    return order


def confirm_order_with_payment(db: Session, order_id: int, user_id: int, method: str) -> tuple[Order, Payment]:
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user_id).first()
    if not order:
        raise CustomException("Order not found", status.HTTP_404_NOT_FOUND)

    order.status = "confirmed"

    payment = Payment(
        user_id=user_id,
        order_id=order.id,
        currency="INR",
        method=method,
        status="pending",
        transaction_id=f"TXN-{order.id}",
        amount=order.total_amount,
    )
    db.add(payment)

    db.commit()
    db.refresh(order)
    db.refresh(payment)

    return order, payment
