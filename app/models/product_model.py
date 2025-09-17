from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.configs.database import Base
from sqlalchemy.orm import relationship


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))


    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    media = relationship("Media", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")
    order_items = relationship("OrderItem", back_populates="product", cascade="all, delete-orphan")
    inventory = relationship("ProductInventory", back_populates="product", uselist=False)
    inventory_logs = relationship("InventoryHistory", back_populates="product")