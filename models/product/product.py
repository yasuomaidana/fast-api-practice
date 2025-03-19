from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship

from .product_type import ProductType


class Product(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    productType: ProductType
    
    __table_args__ = (UniqueConstraint("name","productType"),)
    
    purchased_item: "PurchasedItem" = Relationship(back_populates="product")
    
