from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductOut
from app.services.product_service import  (
    create_product, get_product, get_all_products,
    update_product, delete_product
)


router = APIRouter()

@router.post("/", response_model=ProductOut)
def create(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.get("/{product_id}", response_model=ProductOut)
def read(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/", response_model=list[ProductOut])
def read_all(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.put("/{product_id}", response_model=ProductOut)
def update(product_id: int, updates: ProductUpdate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, updates)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}", response_model=ProductOut)
def delete(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

