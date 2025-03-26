import os
from unittest import TestCase, mock

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, delete

from models import RolePermission, Role, Permission
from models.security.permission.permission_type import PermissionType
from models.security.role.role_type import RoleType
from repository import RoleRepository, PermissionRepository
from repository.security.role_permission_repository import RolePermissionRepository
from settings import DatabaseSettings


class TestRolePermissionRepository(TestCase):

    @classmethod
    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUpClass(cls):
        cls.engine = create_engine(DatabaseSettings().dsn)
        SQLModel.metadata.create_all(cls.engine)
        cls.role_repository = RoleRepository(cls.engine)
        cls.permission_repository = PermissionRepository(cls.engine)
        cls.repository = RolePermissionRepository(cls.engine)

    def setUp(self):
        self.permission_repository.engine = self.engine
        self.role_repository.engine = self.engine
        self.repository.engine = self.engine
        with Session(self.engine) as session:
            self.role_repository.create(RoleType.ADMIN, session=session)
            self.role_repository.create(RoleType.USER, session=session)
            self.permission_repository.create(PermissionType.CREATE_INVOICE, session=session)
            self.permission_repository.create(PermissionType.DELETE_INVOICE, session=session)
            self.permission_repository.create(PermissionType.READ_INVOICE, session=session)
            self.permission_repository.create(PermissionType.UPDATE_INVOICE, session=session)
            session.commit()

    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            for model in [Role, Permission, RolePermission]:
                session.exec(delete(model))
            session.commit()

    def test_create(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        admin_role = self.role_repository.get(RoleType.ADMIN)

        self.repository.create(admin_role, read_permission, session=None)
        with Session(self.engine) as session:
            updated_admin = self.role_repository.get(RoleType.ADMIN, session=session)
            session.refresh(updated_admin, ["permissions"])
        session.close()

        self.assertEqual(len(updated_admin.permissions), 1)
        self.assertEqual(updated_admin.permissions[0], read_permission)

    def test_non_annotated(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        admin_role = self.role_repository.get(RoleType.ADMIN)
        self.repository.create(admin_role.id, read_permission.id, session=None)
        created = self.repository.get(admin_role.id, read_permission.id, session=None)
        self.assertIsNotNone(created)

    def test_create_from_permissions(self):
        admin_role = self.role_repository.get(RoleType.ADMIN)
        with Session(self.engine) as session:
            read_permission = self.permission_repository.get(PermissionType.READ_INVOICE, session=session)
            read_permission.roles = [admin_role]
            session.add(read_permission)
            session.commit()
            session.refresh(read_permission, ["roles"])
        self.assertEqual(len(read_permission.roles), 1)

    def test_create_from_roles(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        with Session(self.engine) as session:
            admin_role = self.role_repository.get(RoleType.ADMIN, session=session)
            admin_role.permissions = [read_permission]
            session.add(admin_role)
            session.commit()
            session.refresh(admin_role, ["permissions"])
        session.close()
        stored = self.repository.get(admin_role, read_permission, session=None)
        self.assertIsNotNone(stored)

    def test_assign_multiple_roles_to_permission(self):
        admin_role = self.role_repository.get(RoleType.ADMIN)
        user_role = self.role_repository.get(RoleType.USER)

        with Session(self.engine) as session:
            read_permission = self.permission_repository.get(PermissionType.READ_INVOICE, session=session)
            read_permission.roles.extend([admin_role, user_role])
            session.refresh(read_permission, ["roles"])
        self.assertEqual(len(read_permission.roles), 2)
        
    def test_assign_multiple_permissions_to_role(self):
        read_permission = self.permission_repository.get(PermissionType.READ_INVOICE)
        delete_permission = self.permission_repository.get(PermissionType.DELETE_INVOICE)
        admin_role = self.role_repository.get(RoleType.ADMIN)

        with Session(self.engine) as session:
            self.repository.create(admin_role.id, read_permission.id, session=session)
            self.repository.create(admin_role.id, delete_permission.id, session=session)
            session.commit()
        with Session(self.engine) as session:
            admin_role = self.role_repository.get(RoleType.ADMIN, session=session)
            session.refresh(admin_role, ["permissions"])
        self.assertEqual(len(admin_role.permissions), 2)
