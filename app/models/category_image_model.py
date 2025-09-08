from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.configs.database import Base

class CategoryImage(Base):
    __tablename__ = "category_images"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))

    category = relationship("Category", back_populates="images")
