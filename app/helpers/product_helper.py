from sqlalchemy.orm import Session
from ..models.product_model import Product
from ..models.product_category import Category
from ..schemas.product_schema import ProductCreate, ProductUpdate
from typing import Optional, List
from sqlalchemy import or_ 


def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()


def create_product(db: Session, product_data: ProductCreate):
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        return None
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, product: Product, updates: ProductUpdate):
    if updates.category_id is not None:
        category = db.query(Category).filter(Category.id == updates.category_id).first()
        if not category:
            return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product: Product):
    db.delete(product)
    db.commit()
    return product


def search_products(db: Session, query_text: str, skip: int = 0, limit: int = 100) -> List[Product]:
    query = db.query(Product).join(Category, isouter=True)

    query = query.filter(
        or_(
            Product.name.ilike(f"%{query_text}%"),
            Product.sku.ilike(f"%{query_text}%"),
            Category.name.ilike(f"%{query_text}%")
        )
    )

    return query.offset(skip).limit(limit).all()

def filter_products(
    db: Session,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    in_stock: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100
) -> List[Product]:
    query = db.query(Product)

    if category_id:
        query = query.filter(Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    if in_stock is True:
        query = query.filter(Product.stock > 0)
    elif in_stock is False:
        query = query.filter(Product.stock == 0)

    return query.offset(skip).limit(limit).all()