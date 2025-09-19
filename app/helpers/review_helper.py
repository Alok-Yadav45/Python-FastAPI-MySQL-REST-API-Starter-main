from sqlalchemy.orm import Session
from app.models.review_model import Review
from app.helpers.exceptions import CustomException
from fastapi import status


def create_review(db: Session, user_id: int, product_id: int, rating: int, comment: str | None) -> Review:
    review = Review(user_id=user_id, product_id=product_id, rating=rating, comment=comment)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review_by_id(db: Session, review_id: int) -> Review:
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise CustomException("Review not found", status.HTTP_404_NOT_FOUND)
    return review


def get_reviews_by_product(db: Session, product_id: int):
    return db.query(Review).filter(Review.product_id == product_id).all()


def get_reviews_by_user(db: Session, user_id: int):
    return db.query(Review).filter(Review.user_id == user_id).all()


def delete_review(db: Session, review_id: int):
    review = get_review_by_id(db, review_id)
    db.delete(review)
    db.commit()
    return review
