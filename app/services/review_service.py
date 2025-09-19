from sqlalchemy.orm import Session
from app.helpers import review_helper
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from app.schemas.review_schema import ReviewCreate, ReviewOut


def add_review(db: Session, review_data: ReviewCreate, user_id: int):
    review = review_helper.create_review(
        db, user_id=user_id, product_id=review_data.product_id,
        rating=review_data.rating, comment=review_data.comment
    )
    return success_response(
        data=ReviewOut.from_orm(review),
        message="Review added successfully"
    )


def get_review(db: Session, review_id: int):
    review = review_helper.get_review_by_id(db, review_id)
    return success_response(
        data=ReviewOut.from_orm(review),
        message="Review retrieved successfully"
    )


def list_reviews_by_product(db: Session, product_id: int):
    reviews = review_helper.get_reviews_by_product(db, product_id)
    return success_response(
        data=[ReviewOut.from_orm(r) for r in reviews],
        message="Product reviews retrieved successfully"
    )


def list_reviews_by_user(db: Session, user_id: int):
    reviews = review_helper.get_reviews_by_user(db, user_id)
    return success_response(
        data=[ReviewOut.from_orm(r) for r in reviews],
        message="User reviews retrieved successfully"
    )


def delete_review(db: Session, review_id: int, token_data: dict):
    review = review_helper.get_review_by_id(db, review_id)

    
    if token_data["role"] != "admin" and review.user_id != token_data["user_id"]:
        raise CustomException("Not authorized to delete this review", 403)

    review_helper.delete_review(db, review_id)
    return success_response(message="Review deleted successfully")
