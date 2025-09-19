from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func
from sqlalchemy.orm import relationship
from app.configs.database import Base

class InventoryHistory(Base):
    __tablename__ = "inventory_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    change = Column(Integer, nullable=False)  
    action = Column(String(50), nullable=False) 
    updated_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="inventory_logs")
