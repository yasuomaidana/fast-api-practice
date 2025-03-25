from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .permission_type import PermissionType


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    permission: PermissionType

    roles: list["RolePermission"] = Relationship(back_populates="permission")
