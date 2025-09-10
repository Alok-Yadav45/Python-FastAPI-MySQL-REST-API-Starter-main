from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.services import media_service
from app.schemas.media_schema import MediaOut, APIResponse
from typing import List

router = APIRouter()

@router.post("/upload", response_model=APIResponse[List[MediaOut]])
async def upload_file(
    entity_type: str = Form(...),  
    entity_id: int = Form(...),
    file_type: str = Form(...),
    file: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
   
   

    return media_service.upload_media_files(db, file, entity_type, entity_id, file_type)



@router.put("/media/{media_id}", response_model=APIResponse[MediaOut])
async def update_media(
    media_id: int,
    file_url: str = Form(None),
    file_type: str = Form(None),
    filename: str = Form(None),
    new_file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    update_data = {
        "file_url": file_url,
        "file_type": file_type,
        "filename": filename
    }
    return media_service.update_media(db, media_id, update_data, new_file)


@router.delete("/media/{media_id}", response_model=APIResponse)
async def delete_media(media_id: int, db: Session = Depends(get_db)):
    return media_service.delete_media(db, media_id)