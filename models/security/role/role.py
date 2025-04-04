from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .role_type import RoleType
from .. import RolePermission


class Role(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    role: RoleType

    permissions: list["Permission"] = Relationship(back_populates="roles", link_model=RolePermission)
