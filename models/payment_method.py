from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class PaymentMethod(SQLModel, table=True):
    __tablename__ = "payment_method"
    id: Optional[int] = Field(primary_key=True)
    name: str
    
    invoices: List["Invoice"] = Relationship(back_populates="payment_method")
