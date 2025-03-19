from typing import Union

from sqlalchemy import Engine
from sqlmodel import Session

from dto.create_place_dto import CreatePlaceDto
from models import Place
from repository import PlaceRepository
from repository.utils import transactional, with_session
from settings import engine


class PlaceService:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(PlaceService, cls).__new__(cls)
            cls._instance.engine = _engine
            cls._instance.place_repository = PlaceRepository(_engine)
        return cls._instance

    def get_all(self, session: Session = None):
        return self.place_repository.get_places(session=session)

    def create(self, place: Union[Place, CreatePlaceDto], session: Session = None):
        if isinstance(place, CreatePlaceDto):
            place = place.to_place_model()
        return self.place_repository.create_place(place, session=session)

    @transactional
    def delete(self, place: Union[Place, int], session: Session = None):
        if isinstance(place, int):
            place = self.place_repository.get_place_by_id(place, session=session)
        if isinstance(place, Place):
            self.place_repository.delete_place(place, session=session)
    
    def find_by_id(self, place_id: int, session: Session = None):
        return self.place_repository.get_place_by_id(place_id, session=session)
