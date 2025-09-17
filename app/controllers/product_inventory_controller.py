from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.product_inventory_schema import ProductInventoryCreate, ProductInventoryOut
from app.schemas.inventory_history_schema import InventoryHistoryOut
from app.services import product_inventory_service

router = APIRouter()


@router.post("/", response_model=ProductInventoryOut)
def create_inventory(data: ProductInventoryCreate, db: Session = Depends(get_db)):
    """Create inventory record for a product"""
    return product_inventory_service.create_inventory(db, data)


@router.post("/place-order/{product_id}/{quantity}", response_model=ProductInventoryOut)
def place_order(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Reduce stock when order is placed"""
    return product_inventory_service.place_order(db, product_id, quantity)


@router.post("/cancel-order/{product_id}/{quantity}", response_model=ProductInventoryOut)
def cancel_order(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Increase stock when order is cancelled/returned"""
    return product_inventory_service.cancel_or_return_order(db, product_id, quantity)


@router.post("/restock/{product_id}/{quantity}", response_model=ProductInventoryOut)
def restock(product_id: int, quantity: int, db: Session = Depends(get_db)):
    """Increase stock when items are restocked"""
    return product_inventory_service.restock(db, product_id, quantity)

@router.get("/{product_id}", response_model=ProductInventoryOut)
def get_inventory(product_id: int, db: Session = Depends(get_db)):
    """Get current stock of a product"""
    return product_inventory_service.get_inventory(db, product_id)


@router.get("/history/{product_id}", response_model=list[InventoryHistoryOut])
def get_inventory_history(product_id: int, db: Session = Depends(get_db)):
    """Get history of stock changes for a product"""
    return product_inventory_service.get_inventory_history(db, product_id)

