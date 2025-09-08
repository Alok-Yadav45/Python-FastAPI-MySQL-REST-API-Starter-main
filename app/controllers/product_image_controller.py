from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services import product_image_service
from app.schemas.product_image_schema import ProductImageOut, APIResponse

router = APIRouter()

@router.post("/{product_id}", response_model=APIResponse[ProductImageOut])
def upload(product_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return product_image_service.upload_product_image(db, product_id, file)

@router.get("/{product_id}", response_model=APIResponse[list[ProductImageOut]])
def list_images(product_id: int, db: Session = Depends(get_db)):
    return product_image_service.get_images_for_product(db, product_id)
