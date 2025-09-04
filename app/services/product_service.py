from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product_category import Category
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate

def create_product(db: Session, product_data: ProductCreate):
    category = db.query(Category).filter(Category.id == product_data.category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Invalid category_id: category does not exist")

    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def get_all_products(db: Session):
    return db.query(Product).all()

def update_product(db: Session, product_id: int, updates: ProductUpdate):
    product = get_product(db, product_id)
    if not product:
        return None
    
    if updates.category_id is not None:
        category = db.query(Category).filter(Category.id == updates.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail=f"Category with id={updates.category_id} does not exist")
 
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: int):
    product = get_product(db, product_id)
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product