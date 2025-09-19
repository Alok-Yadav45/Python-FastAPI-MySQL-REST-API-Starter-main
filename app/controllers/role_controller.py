from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.configs.database import get_db
from app.schemas.role_schema import RoleCreate
from app.services import role_service
from app.middleware.verify_access_token import verify_access_token
from app.middleware.role_checker import role_checker

router = APIRouter()


@router.post("/", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: create a new role"""
    return role_service.create_role(db, role)


@router.get("/", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def get_roles(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: get all roles"""
    return role_service.get_roles(db)


@router.put("/assign/{user_id}/{role_id}", response_model=dict, dependencies=[Depends(role_checker(["admin"]))])
def assign_role(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_access_token)
):
    """Admin only: assign a role to a user"""
    return role_service.assign_role(db, user_id, role_id)
