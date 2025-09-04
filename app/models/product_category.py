from sqlalchemy import Column, Integer, String
from app.configs.database import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)

    products = relationship("Product", back_populates="category")

