from fastapi import APIRouter

from dto.create_place_dto import CreatePlaceDto
from service import PlaceService

place_router = APIRouter(prefix="/place")

@place_router.post("")
async def create_place(place:CreatePlaceDto):
    place_service = PlaceService()
    return place_service.create_place(place)

@place_router.get("/{place_id}")
async def get_place(place_id: int):
    place_service = PlaceService()
    return place_service.get_place(place_id)