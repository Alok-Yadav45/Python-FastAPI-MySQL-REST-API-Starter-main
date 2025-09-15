from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.media_schema import APIResponse
from app.services import checkout_service

router = APIRouter()

@router.post("/checkout", response_model=APIResponse)
def checkout(user_id: int, db: Session = Depends(get_db)):
    return checkout_service.checkout(db, user_id)


@router.post("/orders/{order_id}/confirm", response_model=APIResponse)
def confirm_order(order_id: int, user_id: int, db: Session = Depends(get_db)):
    return checkout_service.confirm_order(db, order_id, user_id)
