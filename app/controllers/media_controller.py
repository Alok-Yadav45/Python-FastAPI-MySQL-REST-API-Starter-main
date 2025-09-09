from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services import media_service
from app.schemas.media_schema import MediaOut, APIResponse

router = APIRouter()

@router.post("/upload", response_model=APIResponse[MediaOut])
async def upload_file(
    entity_type: str = Form(...),  
    entity_id: int = Form(...),
    file_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
   
   

    return media_service.upload_media(db, file, entity_type, entity_id, file_type)


@router.delete("/media/{media_id}", response_model=APIResponse)
async def delete_media(media_id: int, db: Session = Depends(get_db)):
    return media_service.delete_media(db, media_id)