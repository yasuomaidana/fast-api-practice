from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .role_type import RoleType


class Role(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    role: RoleType

    permissions: list["RolePermission"] = Relationship(back_populates="role")
    accounts: list["AccountRole"] = Relationship(back_populates="role")
