from sqlalchemy.orm import Session
from app.models.product_inventory_model import ProductInventory
from app.models.inventory_history_model import InventoryHistory
from app.helpers.exceptions import CustomException
from fastapi import status


def create_inventory(db: Session, product_id: int, stock: int) -> ProductInventory:
    inventory = ProductInventory(product_id=product_id, stock=stock)
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory


def get_inventory_by_product(db: Session, product_id: int) -> ProductInventory:
    inventory = db.query(ProductInventory).filter_by(product_id=product_id).first()
    if not inventory:
        raise CustomException("Inventory not found", status.HTTP_404_NOT_FOUND)
    return inventory


def update_stock(db: Session, product_id: int, change: int, action: str) -> ProductInventory:
    inventory = get_inventory_by_product(db, product_id)
    new_stock = inventory.stock + change
    if new_stock < 0:
        raise CustomException("Insufficient stock", status.HTTP_400_BAD_REQUEST)

    inventory.stock = new_stock
    db.add(InventoryHistory(product_id=product_id, change=change, action=action))
    db.commit()
    db.refresh(inventory)
    return inventory


def get_inventory_history(db: Session, product_id: int):
    return db.query(InventoryHistory).filter_by(product_id=product_id).all()
