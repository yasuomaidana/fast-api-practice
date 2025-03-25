from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class PermissionType(Enum):
    READ_INVOICE = "read:invoice"
    CREATE_INVOICE = "create:invoice"
    UPDATE_INVOICE = "update:invoice"
    DELETE_INVOICE = "delete:invoice"


class Permission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    permission: PermissionType

    roles: list["RolePermission"] = Relationship(back_populates="permission")
