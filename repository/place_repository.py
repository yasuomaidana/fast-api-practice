from sqlalchemy import Engine
from sqlmodel import Session, select

from models import Place
from repository.utils import create_entity, with_session, transactional
from settings import engine


class PlaceRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(PlaceRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    @create_entity
    def create_place(self, place: Place, session: Session = None):
        return session.add(place)

    @with_session
    def get_place_by_id(self, place_id: int, session: Session = None):
        return session.get(Place, place_id)

    @with_session
    def get_places(self, session: Session = None):
        statement = select(Place)
        return session.exec(statement).all()

    @transactional
    def delete_place(self, place: Place, session: Session = None):
        return session.delete(place)
