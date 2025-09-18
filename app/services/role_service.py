from sqlalchemy.orm import Session
from app.models.role_model import Role
from app.models.user_model import User
from app.schemas.role_schema import RoleCreate

def create_role(db: Session, role: RoleCreate):
    db_role = Role(role=role.role)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def assign_role(db: Session, user_id: int, role_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    role = db.query(Role).filter(Role.id == role_id).first()

    if not user or not role:
        return None

    user.role_id = role.id
    db.commit()
    db.refresh(user)
    return user
