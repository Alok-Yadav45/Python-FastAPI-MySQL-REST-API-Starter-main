from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services import category_image_service
from app.schemas.category_image_schema import CategoryImageOut, APIResponse

router = APIRouter()

@router.post("/{category_id}", response_model=APIResponse[CategoryImageOut])
def upload(category_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    return category_image_service.upload_category_image(db, category_id, file)

@router.get("/{category_id}", response_model=APIResponse[list[CategoryImageOut]])
def list_images(category_id: int, db: Session = Depends(get_db)):
    return category_image_service.get_images_for_category(db, category_id)
