from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class RoleType(Enum):
    ADMIN = "admin"
    USER = "user"


class Role(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    role: RoleType

    permissions: list["RolePermission"] = Relationship(back_populates="role")
