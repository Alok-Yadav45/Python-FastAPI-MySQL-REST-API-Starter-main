from sqlalchemy.orm import Session
from app.helpers import role_helper
from app.helpers.response_helper import success_response
from app.schemas.role_schema import RoleCreate, RoleOut


def create_role(db: Session, role: RoleCreate):
    new_role = role_helper.create_role(db, role.role)
    return success_response(
        data=RoleOut.from_orm(new_role),
        message="Role created successfully"
    )


def get_roles(db: Session):
    roles = role_helper.get_roles(db)
    return success_response(
        data=[RoleOut.from_orm(r) for r in roles],
        message="Roles retrieved successfully"
    )


def assign_role(db: Session, user_id: int, role_id: int):
    updated_user = role_helper.assign_role(db, user_id, role_id)
    return success_response(
        data={"user_id": updated_user.id, "role": updated_user.role.role},
        message="Role assigned successfully"
    )
