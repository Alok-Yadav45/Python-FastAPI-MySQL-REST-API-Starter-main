from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Shipping(Base):
    __tablename__ = "shipping"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    address = Column(String(255), nullable=False)
    courier = Column(String(100), nullable=False)
    tracking_number = Column(String(100), unique=True, nullable=True)
    status = Column(String(50), default="preparing")

    order = relationship("Order", back_populates="shipping")
