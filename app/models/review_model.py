from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from app.configs.database import Base
from sqlalchemy.orm import relationship

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(500), nullable=True)
    timestamp = Column(DateTime, server_default=func.now())


    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")  # ⬅️ Must match Product.reviews
