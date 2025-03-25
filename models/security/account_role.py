from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Relationship, Field


class AccountRole(SQLModel, table=True):
    __tablename__ = "account_role"
    
    account_id: int = Field(foreign_key="account.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)

    account: "Account" = Relationship(back_populates="roles")
    role: "Role" = Relationship(back_populates="accounts")
    
    __table_args__ = (UniqueConstraint("account_id", "role_id"),)
    