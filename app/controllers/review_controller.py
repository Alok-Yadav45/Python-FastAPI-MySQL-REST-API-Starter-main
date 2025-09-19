from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.review_schema import ReviewCreate
from app.services import review_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=dict)
def add_review(
    review_data: ReviewCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Users can add reviews"""
    return review_service.add_review(db, review_data, token_data["user_id"])


@router.get("/{review_id}", response_model=dict)
def get_review(
    review_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Any logged-in user can fetch a review"""
    return review_service.get_review(db, review_id)


@router.get("/product/{product_id}", response_model=dict)
def list_reviews_by_product(
    product_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Any logged-in user can see reviews for a product"""
    return review_service.list_reviews_by_product(db, product_id)


@router.get("/user/{user_id}", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def list_reviews_by_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    """Admin only: list reviews by a specific user"""
    return review_service.list_reviews_by_user(db, user_id)


@router.delete("/{review_id}", response_model=dict)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Users can delete their own reviews; Admins can delete any"""
    return review_service.delete_review(db, review_id, token_data)
