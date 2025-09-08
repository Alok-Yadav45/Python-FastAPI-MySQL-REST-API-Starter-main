import os, shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile, status
from app.models.product_model import Product
from app.helpers import product_image_helper
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from app.schemas.product_image_schema import ProductImageOut

UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_product_image(db: Session, product_id: int, file: UploadFile):
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise CustomException("Product not found", status.HTTP_404_NOT_FOUND)

   
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    image = product_image_helper.create_product_image(db, product_id, f"/{file_path}")

    return success_response(
        data=ProductImageOut.from_orm(image),
        message="Product image uploaded successfully"
    )

def get_images_for_product(db: Session, product_id: int):
    images = product_image_helper.get_product_images(db, product_id)
    return success_response(
        data=[ProductImageOut.from_orm(img) for img in images],
        message="Product images fetched successfully"
    )
