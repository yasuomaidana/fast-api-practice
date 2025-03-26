from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .permission_type import PermissionType
from .. import RolePermission


class Permission(SQLModel, table=True):
    """
    Represents a permission in the system.

    Attributes:
        id (Optional[int]): The primary key of the permission.
        permission (PermissionType): The type of permission.
        roles (list["RolePermission"]): The roles associated with this permission.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    permission: PermissionType

    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)
