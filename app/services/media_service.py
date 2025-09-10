import shutil, os, uuid
from pathlib import Path
from sqlalchemy.orm import Session
from fastapi import UploadFile, status
from app.helpers import media_helper
from app.models.product_model import Product
from app.models.product_category import Category
from app.schemas.media_schema import MediaCreate, MediaOut
from app.helpers.response_helper import success_response
from app.helpers.exceptions import CustomException

BASE_UPLOAD_DIR = Path("uploads/media")
BASE_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    "image": [".jpg", ".jpeg", ".png", ".gif"],
    "video": [".mp4", ".avi", ".mov"],
    "document": [".pdf", ".docx", ".xlsx", ".txt"],
}

MAX_FILE_SIZE_MB = {
    "image": 15,
    "video": 50,
    "document": 10,
    "other": 20, 
}


def _validate_file(file: UploadFile, file_type: str):
    """Validate file extension and size"""
    ext = os.path.splitext(file.filename)[1].lower()

    if file_type != "other" and ext not in ALLOWED_EXTENSIONS[file_type]:
        raise CustomException(
            message=f"Invalid file extension '{ext}' for {file_type}. Allowed: {ALLOWED_EXTENSIONS[file_type]}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell() / (1024 * 1024)
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE_MB.get(file_type, 20):
        raise CustomException(
            message=f"File too large ({file_size:.2f} MB). Max {MAX_FILE_SIZE_MB.get(file_type, 20)} MB for {file_type}",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


def upload_media_files(db: Session, files: list[UploadFile], entity_type: str, entity_id: int, file_type: str):
   

    product_id, category_id = None, None


    if entity_type == "product":
        if not db.query(Product).filter(Product.id == entity_id).first():
            raise CustomException("Product not found", status.HTTP_404_NOT_FOUND)
        product_id = entity_id
    elif entity_type == "category":
        if not db.query(Category).filter(Category.id == entity_id).first():
            raise CustomException("Category not found", status.HTTP_404_NOT_FOUND)
        category_id = entity_id
    elif entity_type not in ["user", "video"]:
        raise CustomException("Invalid entity type", status.HTTP_400_BAD_REQUEST)


    if file_type not in ["image", "video", "document", "other"]:
        raise CustomException("Invalid file type", status.HTTP_400_BAD_REQUEST)

    uploaded_media = []

    for file in files:
        _validate_file(file, file_type)

        ext = os.path.splitext(file.filename)[1].lower()
        unique_name = f"{uuid.uuid4()}{ext}"

        upload_dir = BASE_UPLOAD_DIR / entity_type / str(entity_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / unique_name
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        media_data = MediaCreate(
            file_url=f"/media/{entity_type}/{entity_id}/{unique_name}",
            file_type=file_type,
            filename=file.filename, 
            product_id=product_id,
            category_id=category_id,
        )
        media = media_helper.create_media(db, media_data)
        uploaded_media.append(MediaOut.from_orm(media))

    return success_response(
        data=uploaded_media,
        message=f"{len(uploaded_media)} {file_type}(s) uploaded successfully",
    )

def update_media(db: Session, media_id: int, update_data: dict, new_file: UploadFile = None):
    

    media = media_helper.get_media(db, media_id)
    if not media:
        raise CustomException("Media not found", status.HTTP_404_NOT_FOUND)

    
    if new_file:
        ext = os.path.splitext(new_file.filename)[1].lower()
        unique_name = f"{uuid.uuid4()}{ext}"

        
        entity_type = "product" if media.product_id else "category"
        entity_id = media.product_id or media.category_id

        upload_dir = BASE_UPLOAD_DIR / entity_type / str(entity_id)
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / unique_name
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(new_file.file, buffer)

        
        old_file_path = Path("uploads") / media.file_url.lstrip("/")
        if old_file_path.exists():
            old_file_path.unlink()

        
        media.file_url = f"/media/{entity_type}/{entity_id}/{unique_name}"
        media.filename = new_file.filename

   
    for field, value in update_data.items():
        if value is not None:
            setattr(media, field, value)

    db.commit()
    db.refresh(media)

    return success_response(
        data=MediaOut.from_orm(media),
        message="Media updated successfully"
    )


def delete_media(db: Session, media_id: int):
   
    media = media_helper.get_media(db, media_id)
    if not media:
        raise CustomException("Media not found", status.HTTP_404_NOT_FOUND)

    file_path = Path("uploads") / media.file_url.lstrip("/")

    if file_path.exists():
        file_path.unlink()

    media_helper.delete_media(db, media)
    return success_response(message="Media deleted successfully")
