import os
from unittest import TestCase, mock

from sqlmodel import SQLModel, Session, delete, create_engine

from models import Role
from models.security.role.role_type import RoleType
from repository import RoleRepository
from settings import DatabaseSettings


class TestRoleRepository(TestCase):
    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUp(self):
        self.engine = create_engine(DatabaseSettings().dsn)
        SQLModel.metadata.create_all(self.engine)
        self.repository = RoleRepository(self.engine)

    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            statement = delete(Role)
            session.exec(statement)
            session.commit()
        session.commit()
        
    def test_create(self):
        role_type = RoleType.ADMIN
        role = Role(role=role_type)
        with Session(self.engine) as session:
            self.repository.create(role, session)
            session.commit()
            session.refresh(role)
            self.assertIsNotNone(role.id)
            self.assertEqual(role.role, role_type)
            
    def test_create_annotated(self):
        role_type = RoleType.ADMIN
        role = self.repository.create(role_type, session=None)
        self.assertIsNotNone(role.id)
        
    def test_get(self):
        self.repository.create(Role(role=RoleType.ADMIN), session=None)
        role = self.repository.get(RoleType.ADMIN, session=None)
        self.assertIsNotNone(role)