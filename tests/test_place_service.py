import os
from unittest import TestCase, mock

from sqlalchemy import create_engine, delete
from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, Session

from models import Place
from models.place.place_type import PlaceType
from service import PlaceService
from settings.database_settings import DatabaseSettings


class TestPlaceService(TestCase):
    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUp(self):
        TestPlaceService.engine = create_engine(DatabaseSettings().dsn)
        SQLModel.metadata.create_all(self.engine)
        
    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            statement = delete(Place)
            session.exec(statement)
            session.commit()
        session.commit()
        

    # Execute after all tests
    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()

    def test__create_place(self):
        place_service = PlaceService(self.engine)
        to_create = Place(name="test_create", place_type=PlaceType.STORE)
        place_service.create(to_create)
        self.assertIsNotNone(to_create.id)

    def test__create_duplicated(self):
        place_service = PlaceService(self.engine)
        to_create = Place(name="test", place_type=PlaceType.STORE)
        place_service.create(to_create)
        with self.assertRaises(IntegrityError):
            to_create2 = Place(name="test", place_type=PlaceType.STORE)
            place_service.create(to_create2)

    def test__create_no_refresh(self):
        place_service = PlaceService(self.engine)
        with Session(self.engine) as session:
            to_create = Place(name="test", place_type=PlaceType.STORE)
            place_service.create(to_create, session)
            self.assertIsNone(to_create.id)
            session.commit()
            session.refresh(to_create)
            self.assertIsNotNone(to_create.id)
