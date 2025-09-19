from sqlalchemy.orm import Session
from app.models.role_model import Role
from app.models.user_model import User
from app.helpers.exceptions import CustomException
from fastapi import status


def create_role(db: Session, role_name: str) -> Role:
    if db.query(Role).filter(Role.role == role_name).first():
        raise CustomException("Role already exists", status.HTTP_400_BAD_REQUEST)

    db_role = Role(role=role_name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_roles(db: Session):
    return db.query(Role).all()


def assign_role(db: Session, user_id: int, role_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()

    if not user:
        raise CustomException("User not found", status.HTTP_404_NOT_FOUND)
    if not role:
        raise CustomException("Role not found", status.HTTP_404_NOT_FOUND)

    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user
