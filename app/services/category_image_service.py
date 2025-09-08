import os, shutil
from sqlalchemy.orm import Session
from fastapi import UploadFile, status
from app.models.product_category import Category
from app.helpers import category_image_helper
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException
from app.schemas.category_image_schema import CategoryImageOut

UPLOAD_DIR = "uploads/categories"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def upload_category_image(db: Session, category_id: int, file: UploadFile):

    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)


    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    image = category_image_helper.create_category_image(db, category_id, f"/{file_path}")

    return success_response(
        data=CategoryImageOut.from_orm(image),
        message="Category image uploaded successfully"
    )

def get_images_for_category(db: Session, category_id: int):
    images = category_image_helper.get_category_images(db, category_id)
    return success_response(
        data=[CategoryImageOut.from_orm(img) for img in images],
        message="Category images fetched successfully"
    )
