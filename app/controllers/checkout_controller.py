from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.media_schema import APIResponse
from app.services import checkout_service
from app.middleware.verify_access_token import verify_access_token  
from app.schemas.payment_schema import PaymentCreate 

router = APIRouter()

@router.post("/checkout", response_model=APIResponse)
def checkout(db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return checkout_service.checkout(db, user_id)



@router.post("/orders/{order_id}/confirm", response_model=APIResponse)
def confirm_order(  order_id: int,
    data: PaymentCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return checkout_service.confirm_order(db, order_id, user_id, method=data.method)




