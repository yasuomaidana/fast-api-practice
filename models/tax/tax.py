from typing import Optional

from sqlmodel import SQLModel, Field, Relationship

from .tax_type import TaxType


class Tax(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    tax_type: TaxType
    value: float
    invoiceId: Optional[int] = Field(default=TaxType.VAT, foreign_key="invoice.id")
    
    invoice: "Invoice" = Relationship(back_populates="taxes")
