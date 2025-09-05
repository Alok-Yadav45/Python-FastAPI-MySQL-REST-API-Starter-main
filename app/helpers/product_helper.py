from sqlalchemy.orm import Session
from app.models.product_model import Product
from app.models.product_category import Category
from app.schemas.product_schema import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def create_product(db: Session, product_data: ProductCreate):
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not Category:
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
