from sqlalchemy import Engine
from sqlmodel import Session

from dto.create_place_dto import CreatePlaceDto
from models import Place
from service.utils import with_session
from settings.database_settings import engine


class PlaceService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PlaceService, cls).__new__(cls)

        return cls._instance
    
    def __init__(self):
        self.engine: Engine = engine

    @with_session
    def get_place(self, place_id: int, session: Session = None):
        return session.get(Place, place_id)
    
    @with_session
    def create_place(self, place: CreatePlaceDto, session: Session = None):
        place = place.to_place_model()
        session.add(place)
        session.commit()
        session.refresh(place)
        return place
