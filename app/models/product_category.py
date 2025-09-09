from sqlalchemy import Column, Integer, String, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),nullable=False, unique=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    children = relationship("Category", backref="parent", remote_side=[id])

    products = relationship("Product", back_populates="category")

     
    media = relationship("Media", back_populates="category", cascade="all, delete-orphan")


