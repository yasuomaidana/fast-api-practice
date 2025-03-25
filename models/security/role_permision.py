from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


class RolePermission(SQLModel, table=True):
    __tablename__ = "role_permission"
    
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    permission_id: int = Field(foreign_key="permission.id", primary_key=True)

    __table_args__ = (UniqueConstraint("role_id", "permission_id"),)

    role: "Role" = Relationship(back_populates="permissions")
    permission: "Permission" = Relationship(back_populates="roles")
