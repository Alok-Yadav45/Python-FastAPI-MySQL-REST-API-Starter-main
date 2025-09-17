from sqlalchemy.orm import Session
from app.models.review_model import Review
from app.schemas.review_schema import ReviewCreate
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from fastapi import status

def add_review(db: Session, review_data: ReviewCreate, user_id: int):
    review = Review(user_id=user_id, **review_data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return success_response(data=review, message="Review added successfully")

def get_review(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise CustomException("Review not found", status.HTTP_404_NOT_FOUND)
    return success_response(data=review, message="Review retrieved successfully")

def list_reviews_by_product(db: Session, product_id: int):
    reviews = db.query(Review).filter(Review.product_id == product_id).all()
    return success_response(data=reviews, message="Product reviews retrieved successfully")

def list_reviews_by_user(db: Session, user_id: int):
    reviews = db.query(Review).filter(Review.user_id == user_id).all()
    return success_response(data=reviews, message="User reviews retrieved successfully")

def delete_review(db: Session, review_id: int, user_id: int):
    review = db.query(Review).filter(Review.id == review_id, Review.user_id == user_id).first()
    if not review:
        raise CustomException("Review not found or not owned by user", status.HTTP_404_NOT_FOUND)

    db.delete(review)
    db.commit()
    return success_response(message="Review deleted successfully")
