from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class PlaceType(Enum):
    BAR = "bar"
    RESTAURANT = "restaurant"
    HOTEL = "hotel"
    CONVENIENCE_STORE = "convenience_store"
    GOVERNMENT = "government"
    HOSPITAL = "hospital"
    STORE = "store"
    SCHOOL = "school"
    PHARMACY = "pharmacy"
    


class Place(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    name: str
    place_type: PlaceType
