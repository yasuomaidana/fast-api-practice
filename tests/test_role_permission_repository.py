import os
from time import sleep
from unittest import TestCase, mock

from sqlalchemy import create_engine, StaticPool
from sqlmodel import SQLModel, Session, delete

from models import RolePermission, Role, Permission
from models.security.permission.permission_type import PermissionType
from models.security.role.role_type import RoleType
from repository import RoleRepository, PermissionRepository
from repository.security.role_permission_repository import RolePermissionRepository


class TestRolePermissionRepository(TestCase):

    @classmethod
    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUpClass(cls):
        cls.engine = create_engine("sqlite://", connect_args={"check_same_thread": False},
                                   poolclass=StaticPool)
        SQLModel.metadata.create_all(cls.engine)
        cls.role_repository = RoleRepository(cls.engine)
        cls.permission_repository = PermissionRepository(cls.engine)
        cls.repository = RolePermissionRepository(cls.engine)

        cls.role_repository.create(RoleType.ADMIN)
        cls.role_repository.create(RoleType.USER)
        cls.permission_repository.create(PermissionType.CREATE_INVOICE)
        cls.permission_repository.create(PermissionType.DELETE_INVOICE)
        cls.permission_repository.create(PermissionType.READ_INVOICE)
        cls.permission_repository.create(PermissionType.UPDATE_INVOICE)

    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            statement = delete(RolePermission)
            session.exec(statement)
            session.commit()

    @classmethod
    def tearDownClass(cls):
        with Session(cls.engine) as session:
            session.exec(delete(Role))
            session.exec(delete(Permission))
            session.exec(delete(RolePermission))
            session.commit()
        cls.engine.dispose()

    def test_create(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        admin_role = self.role_repository.get(RoleType.ADMIN)
        self.repository.create(admin_role, read_permission, session=None)
        admin_read = self.repository.get(admin_role.id, read_permission.id)
        self.assertIsNotNone(admin_read)
        self.assertEqual(admin_read.role, admin_role)
        self.assertEqual(admin_read.permission, read_permission)

    def test_get_joined(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        admin_role = self.role_repository.get(RoleType.ADMIN)
        with Session(self.engine) as session:
            self.repository.create(admin_role, read_permission, session=session)
            session.commit()
        with Session(self.engine) as session:
            admin_read = self.repository.get(admin_role.id, read_permission.id, session=session)
        
        self.assertIsNotNone(admin_read)
        
        self.assertEqual(admin_read.role, admin_role)
        self.assertEqual(admin_read.permission, read_permission)
