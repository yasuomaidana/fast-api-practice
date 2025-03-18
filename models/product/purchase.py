from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from models.product.product import Product


class PurchasedItem(SQLModel, table=True):
    __tablename__ = "purchased_item"
    id: Optional[int] = Field(primary_key=True)
    productId: int = Field(foreign_key="product.id")
    quantity: int
    invoiceId: int = Field(foreign_key="invoice.id")
    
    product: Product = Relationship(back_populates="purchased_item")
    invoice: Optional["Invoice"] = Relationship(back_populates="products")
    
