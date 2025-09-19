from sqlalchemy.orm import Session
from app.helpers import product_inventory_helper
from app.helpers.response_helper import success_response
from app.schemas.product_inventory_schema import ProductInventoryCreate, ProductInventoryOut
from app.schemas.inventory_history_schema import InventoryHistoryOut


def create_inventory(db: Session, data: ProductInventoryCreate):
    inventory = product_inventory_helper.create_inventory(db, data.product_id, data.stock)
    return success_response(
        data=ProductInventoryOut.from_orm(inventory),
        message="Inventory created successfully"
    )


def place_order(db: Session, product_id: int, quantity: int):
    inventory = product_inventory_helper.update_stock(db, product_id, -quantity, "order")
    return success_response(
        data=ProductInventoryOut.from_orm(inventory),
        message="Stock reduced for order"
    )


def cancel_or_return_order(db: Session, product_id: int, quantity: int):
    inventory = product_inventory_helper.update_stock(db, product_id, quantity, "cancel/return")
    return success_response(
        data=ProductInventoryOut.from_orm(inventory),
        message="Stock increased due to cancellation/return"
    )


def restock(db: Session, product_id: int, quantity: int):
    inventory = product_inventory_helper.update_stock(db, product_id, quantity, "restock")
    return success_response(
        data=ProductInventoryOut.from_orm(inventory),
        message="Product restocked successfully"
    )


def get_inventory(db: Session, product_id: int):
    inventory = product_inventory_helper.get_inventory_by_product(db, product_id)
    return success_response(
        data=ProductInventoryOut.from_orm(inventory),
        message="Inventory retrieved successfully"
    )


def get_inventory_history(db: Session, product_id: int):
    history = product_inventory_helper.get_inventory_history(db, product_id)
    return success_response(
        data=[InventoryHistoryOut.from_orm(h) for h in history],
        message="Inventory history retrieved successfully"
    )
