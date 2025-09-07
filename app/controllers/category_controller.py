from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryUpdate, APIResponse
from app.services.category_service import (create_category, get_category, get_all_categories, update_category, delete_category,)

router = APIRouter()

@router.post("/", response_model=APIResponse)
def create(category: CategoryCreate, db: Session = Depends(get_db)): 
    return create_category(db, category) 

@router.get("/{category_id}", response_model=APIResponse) 
def read(category_id: int, db: Session = Depends(get_db)):
    return get_category(db, category_id)  
    
@router.get("/", response_model=APIResponse)  
def read_all(db: Session = Depends(get_db)):  
    return get_all_categories(db)  
  
@router.put("/{category_id}", response_model=APIResponse)  
def update(category_id: int, updates: CategoryUpdate, db: Session = Depends(get_db)): 
    return update_category(db, category_id, updates)  
     
@router.delete("/{category_id}", response_model=APIResponse)  
def delete(category_id: int, db: Session = Depends(get_db)):  
    return delete_category(db, category_id)  

