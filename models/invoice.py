from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field, Relationship


class Invoice(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    placeId: int = Field(foreign_key="place.id")
    paymentMethodId: int = Field(foreign_key="payment_method.id")
    date: Optional[datetime] = Field(default_factory=datetime.now)
    
    products: List["PurchasedItem"] = Relationship(back_populates="invoice")
    taxes: List["Tax"] = Relationship(back_populates="invoice")
    payment_method: Optional["PaymentMethod"] = Relationship(back_populates="invoices")
    place: "Place" = Relationship(back_populates="invoices")
    
