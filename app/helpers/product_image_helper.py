from sqlalchemy.orm import Session
from app.models.product_image_model import ProductImage
from app.schemas.product_image_schema import ProductImageCreate

def create_product_image(db: Session, product_id: int, image_url: str):
    image = ProductImage(image_url=image_url, product_id=product_id)
    db.add(image)
    db.commit()
    db.refresh(image)
    return image

def get_product_images(db: Session, product_id: int):
    return db.query(ProductImage).filter(ProductImage.product_id == product_id).all()

def get_product_image(db: Session, image_id: int):
    return db.query(ProductImage).filter(ProductImage.id == image_id).first()

def delete_product_image(db: Session, image: ProductImage):
    db.delete(image)
    db.commit()
    return image
