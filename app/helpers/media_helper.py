from sqlalchemy.orm import Session
from ..models.media_model import Media
from ..schemas.media_schema import MediaCreate


def create_media(db: Session, media_data: MediaCreate):
    media = Media(**media_data.dict())
    db.add(media)
    db.commit()
    db.refresh(media)
    return media


def get_media(db: Session, media_id: int):
    return db.query(Media).filter(Media.id == media_id).first()


def get_media_for_product(db: Session, product_id: int):
    return db.query(Media).filter(Media.product_id == product_id).all()


def get_media_for_category(db: Session, category_id: int):
    return db.query(Media).filter(Media.category_id == category_id).all()


def delete_media(db: Session, media: Media):
    db.delete(media)
    db.commit()
    return media
