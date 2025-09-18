from sqlalchemy.orm import Session
from app.models.role_model import Role

def is_role_exists(db: Session, role_name: str) -> bool:
    return db.query(Role).filter(Role.role == role_name).first() is not None

def get_role_by_name(db: Session, role_name: str) -> Role | None:
    return db.query(Role).filter(Role.role == role_name).first()
