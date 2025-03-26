from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class RolePermission(SQLModel, table=True):
    """
    Represents the association between roles and permissions.
    
    Attributes:
        role_id (int): The ID of the role.
        permission_id (int): The ID of the permission.
    """
    
    __tablename__ = "role_permission"

    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

    __table_args__ = (UniqueConstraint("role_id", "permission_id"),)
