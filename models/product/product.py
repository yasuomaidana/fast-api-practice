from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .product_type import ProductType


class Product(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    productNameId: int = Field(foreign_key="product_name.id")
    productType: ProductType
    price: float
    
    purchased_item: "PurchasedItem" = Relationship(back_populates="product")
    
