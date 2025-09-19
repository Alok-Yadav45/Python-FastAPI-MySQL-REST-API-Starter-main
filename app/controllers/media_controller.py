from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
from app.configs.database import get_db
from app.schemas.media_schema import Media, MediaCreate
from app.services import media_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.post("/upload", response_model=List[Media], dependencies=[Depends(role_checker("admin"))])
async def upload_file(
    entity_type: str = Form(...),
    entity_id: int = Form(...),
    file_type: str = Form(...),
    file: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(verify_access_token)
):
    return media_service.upload_media(db, file, entity_type, entity_id, file_type)


@router.delete("/media/{media_id}", response_model=Media)
def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(verify_access_token),
    _=Depends(role_checker("admin"))
):
    return media_service.delete_media(db, media_id)
