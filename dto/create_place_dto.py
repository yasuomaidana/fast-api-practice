from pydantic import BaseModel

from models import Place
from models.place.place_type import PlaceType


class CreatePlaceDto(BaseModel):
    name: str
    place_type: PlaceType
    
    def to_place_model(self):
        return Place(**self.model_dump())
    
        