from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.review_schema import ReviewCreate, ReviewOut
from app.schemas.media_schema import APIResponse
from app.services import review_service
from app.middleware.verify_access_token import verify_access_token  

router = APIRouter()

@router.post("/reviews", response_model=APIResponse[ReviewOut])
def add_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return review_service.add_review(db, review_data, user_id)

@router.get("/reviews/{review_id}", response_model=APIResponse[ReviewOut])
def get_review(review_id: int, db: Session = Depends(get_db)):
    return review_service.get_review(db, review_id)

@router.get("/reviews/product/{product_id}", response_model=APIResponse[List[ReviewOut]])
def list_reviews_by_product(product_id: int, db: Session = Depends(get_db)):
    return review_service.list_reviews_by_product(db, product_id)

@router.get("/reviews/user/{user_id}", response_model=APIResponse[List[ReviewOut]])
def list_reviews_by_user(user_id: int, db: Session = Depends(get_db)):
    return review_service.list_reviews_by_user(db, user_id)

@router.delete("/reviews/{review_id}", response_model=APIResponse[str])
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    user_id = token_data["user_id"]
    return review_service.delete_review(db, review_id, user_id)
