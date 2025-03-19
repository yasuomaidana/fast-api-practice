from typing import Optional

from pydantic import EmailStr
from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field


class Account(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: EmailStr
    password: str
    
    __table_args__ = (UniqueConstraint("username"),UniqueConstraint("email"))