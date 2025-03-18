from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field

class TaxType(Enum):
    VAT = "VAT"
    INCOME_TAX = "ISR"
    
class Tax(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    tax_type: TaxType
    value: float
    invoiceId: Optional[int] = Field(default=TaxType.VAT, foreign_key="invoice.id")
    