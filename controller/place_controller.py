from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from dto.create_place_dto import CreatePlaceDto
from models import Place
from service import PlaceService

place_router = APIRouter(prefix="/place", tags=["Place"])

@place_router.post("", response_model=Place, responses={400: {"description": "Place already exists"}})
async def create_place(place:CreatePlaceDto):
    try:
        place_service = PlaceService()
        return place_service.create_from_dto(place)
    except IntegrityError:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Place already exists")

@place_router.get("")
async def get_places():
    place_service = PlaceService()
    return place_service.get_places()

@place_router.get("/{place_id}", response_model=Place,responses={404: {"description": "Place not found"}})
async def get_place(place_id: int):
    place_service = PlaceService()
    place = place_service.get_place_by_id(place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place_service.get_place_by_id(place_id)

@place_router.delete("/{place_id}", status_code=HTTP_204_NO_CONTENT,
                     responses={404: {"description": "Place not found"}, 204: {"description": "Item deleted"}})
async def delete_place(place_id: int):
    place_service = PlaceService()
    place = place_service.get_place_by_id(place_id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    place_service.delete_place_by_id(place_id)