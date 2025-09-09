from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    file_url = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)  
    filename = Column(String(255), nullable=False)

    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=True)

    product = relationship("Product", back_populates="media")
    category = relationship("Category", back_populates="media")
