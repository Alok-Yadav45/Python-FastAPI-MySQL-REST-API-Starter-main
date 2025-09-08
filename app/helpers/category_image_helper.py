from sqlalchemy.orm import Session
from app.models.category_image_model import CategoryImage

def create_category_image(db: Session, category_id: int, image_url: str):
    image = CategoryImage(image_url=image_url, category_id=category_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_category_images(db: Session, category_id: int):
    return db.query(CategoryImage).filter(CategoryImage.category_id == category_id).all()

def get_category_image(db: Session, image_id: int):
    return db.query(CategoryImage).filter(CategoryImage.id == image_id).first()

def delete_category_image(db: Session, image: CategoryImage):
    db.delete(image)
    db.commit()
    return image
