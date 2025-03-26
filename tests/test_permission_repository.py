import os
from unittest import TestCase, mock

from sqlmodel import SQLModel, Session, delete, create_engine

from models import Permission
from models.security.permission.permission_type import PermissionType
from repository import PermissionRepository
from settings import DatabaseSettings


class TestPermissionRepository(TestCase):

    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUp(self):
        TestPermissionRepository.engine = create_engine(DatabaseSettings().dsn)
        SQLModel.metadata.create_all(self.engine)
        self.repository = PermissionRepository(self.engine)

    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            statement = delete(Permission)
            session.exec(statement)
            session.commit()
        session.commit()
        
    @classmethod
    def tearDownClass(cls):
        cls.engine.dispose()
    
    def test_create(self):
        permission = Permission(permission=PermissionType.CREATE_INVOICE)
        with Session(self.engine) as session:
            self.repository.create(permission, session)
            session.commit()
            session.refresh(permission)
            self.assertIsNotNone(permission.id)
            self.assertEqual(permission.permission, PermissionType.CREATE_INVOICE)
            
    def test_create_annotated(self):
        permission = self.repository.create(PermissionType.CREATE_INVOICE, session=None)
        self.assertIsNotNone(permission.id)
        
    def test_get(self):
        self.repository.create(Permission(permission=PermissionType.CREATE_INVOICE), session=None)
        permission = self.repository.get(PermissionType.CREATE_INVOICE, session=None)
        self.assertIsNotNone(permission)
        
