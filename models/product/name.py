from typing import Optional

from sqlmodel import SQLModel, Field


class ProductName(SQLModel, table=True):
    __tablename__ = "product_name"
    id: Optional[int] = Field(primary_key=True)
    name: str
    
