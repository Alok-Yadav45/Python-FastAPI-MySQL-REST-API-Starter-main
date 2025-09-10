from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, func
from sqlalchemy.orm import relationship
from app.configs.database import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key = True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable= False)
    status = Column(String(50), default="pending")
    total_amount = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default= func.now(), onupdate=func.now())
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")