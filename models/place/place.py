from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint

from .place_type import PlaceType


class Place(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    place_type: PlaceType
    
    invoices: List["Invoice"] = Relationship(back_populates="place")
    __table_args__ = (UniqueConstraint("name","place_type"),)