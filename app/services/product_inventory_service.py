from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product_inventory_model import ProductInventory
from app.models.inventory_history_model import InventoryHistory
from app.schemas.product_inventory_schema import ProductInventoryCreate

def create_inventory(db: Session, data: ProductInventoryCreate):
    inventory = ProductInventory(product_id=data.product_id, stock=data.stock)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def place_order(db: Session, product_id: int, quantity: int):
    inventory = db.query(ProductInventory).filter_by(product_id=product_id).first()
    if not inventory or inventory.stock < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    inventory.stock -= quantity
    db.add(InventoryHistory(product_id=product_id, change=-quantity, action="order"))
    db.commit()
    db.refresh(inventory)
    return inventory

def cancel_or_return_order(db: Session, product_id: int, quantity: int):
    inventory = db.query(ProductInventory).filter_by(product_id=product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory.stock += quantity
    db.add(InventoryHistory(product_id=product_id, change=quantity, action="cancel"))
    db.commit()
    db.refresh(inventory)
    return inventory

def restock(db: Session, product_id: int, quantity: int):
    inventory = db.query(ProductInventory).filter_by(product_id=product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    inventory.stock += quantity
    db.add(InventoryHistory(product_id=product_id, change=quantity, action="restock"))
    db.commit()
    db.refresh(inventory)
    return inventory

def get_inventory(db: Session, product_id: int):
    inventory = db.query(ProductInventory).filter_by(product_id=product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

def get_inventory_history(db: Session, product_id: int):
    return db.query(InventoryHistory).filter_by(product_id=product_id).all()

