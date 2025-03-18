from fastapi import APIRouter, HTTPException

from dto.create_place_dto import CreatePlaceDto
from models import Place
from service import PlaceService

place_router = APIRouter(prefix="/place", tags=["Place"])

@place_router.post("", response_model=Place)
async def create_place(place:CreatePlaceDto):
    place_service = PlaceService()
    return place_service.create_place(place)

@place_router.get("/{place_id}", response_model=Place,responses={404: {"description": "Item not found"}})
async def get_place(place_id: int):
    place_service = PlaceService()
    place = place_service.get_place(place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Item not found")
    return place_service.get_place(place_id)