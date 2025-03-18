from sqlalchemy import Engine
from sqlmodel import Session, select

from dto.create_place_dto import CreatePlaceDto
from models import Place
from service.utils import with_session, create_entity, transactional
from settings.database_settings import engine


class PlaceService:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(PlaceService, cls).__new__(cls)
            cls._instance.engine = _engine

        return cls._instance

    def __init__(self, _engine: Engine = engine):
        self.engine: Engine = _engine

    @with_session
    def get_place_by_id(self, place_id: int, session: Session = None):
        return session.get(Place, place_id)

    @with_session
    def get_places(self, session: Session = None):
        statement = select(Place)
        return session.exec(statement).all()

    def create_from_dto(self, place: CreatePlaceDto):
        place = place.to_place_model()
        return self._create_place(place)

    @transactional
    def delete_place_by_id(self, place_id: int, session: Session = None):
        place = self.get_place_by_id(place_id, session=session)
        if isinstance(place, Place):
            self._delete_place(place, session=session)

    @with_session
    def _delete_place(self, place: Place, session: Session = None):
        return session.delete(place)

    @create_entity
    def _create_place(self, place: Place, session: Session = None):
        return session.add(place)
