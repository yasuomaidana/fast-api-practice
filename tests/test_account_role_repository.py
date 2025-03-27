import os
from unittest import TestCase, mock

from sqlmodel import create_engine, SQLModel, Session, delete, select

from models import Role, Permission, RolePermission, Account, AccountRole
from models.security.permission.permission_type import PermissionType
from models.security.role.role_type import RoleType
from repository import RoleRepository, PermissionRepository, AccountRoleRepository
from repository.account_repository import AccountRepository
from repository.security.role_permission_repository import RolePermissionRepository
from settings import DatabaseSettings


class TestAccountRoleRepository(TestCase):

    @classmethod
    @mock.patch.dict(os.environ, {"DATABASE_NAME": ":memory:"}, clear=True)
    def setUpClass(cls):
        cls.engine = create_engine(DatabaseSettings().dsn)
        SQLModel.metadata.create_all(cls.engine)
        cls.role_repository = RoleRepository(cls.engine)
        cls.permission_repository = PermissionRepository(cls.engine)
        cls.role_permission_repository = RolePermissionRepository(cls.engine)
        cls.account_role_repository = AccountRoleRepository(cls.engine)
        cls.account_repository = AccountRepository(cls.engine)

    def setUp(self):
        self.role_repository.engine = self.engine
        self.permission_repository.engine = self.engine
        self.permission_repository.engine = self.engine
        self.role_permission_repository.engine = self.engine
        self.account_role_repository.engine = self.engine
        self.account_repository.engine = self.engine

        self.admin_role = self.role_repository.create(RoleType.ADMIN)
        self.user_role = self.role_repository.create(RoleType.USER)

        self.create_invoice_permission = self.permission_repository.create(PermissionType.CREATE_INVOICE)
        self.delete_invoice_permission = self.permission_repository.create(PermissionType.DELETE_INVOICE)
        self.read_invoice_permission = self.permission_repository.create(PermissionType.READ_INVOICE)
        self.update_invoice_permission = self.permission_repository.create(PermissionType.UPDATE_INVOICE)

        self.user1 = self.account_repository.create(Account(username="user1", password="password1", email="a@b.com"))
        self.user2 = self.account_repository.create(Account(username="user2", password="password2", email="c@a.com"))

        with Session(self.engine) as session:
            admin_role = self.role_repository.get(RoleType.ADMIN, session=session)
            user_role = self.role_repository.get(RoleType.USER, session=session)
            admin_role.permissions = [self.create_invoice_permission, self.delete_invoice_permission,
                                      self.read_invoice_permission,
                                      self.update_invoice_permission]
            user_role.permissions = [self.read_invoice_permission]
            session.add(admin_role)
            session.add(user_role)

            session.commit()

    def tearDown(self):
        # Clean up the database
        with Session(self.engine) as session:
            for model in [Role, Permission, RolePermission, Account, AccountRole]:
                session.exec(delete(model))
            session.commit()

    def test_create_user_with_single_role(self):
        account_role = self.account_role_repository.create(self.user1, self.user_role)
        self.assertEqual(len(account_role), 1)

    def test_get_user_roles(self):
        self.account_role_repository.create(self.user1, self.user_role)
        with Session(self.engine) as session:
            user_roles: Account = self.account_repository.find_by_id(self.user1.id, session=session)
            self.assertEqual(len(user_roles.roles), 1)
            session.commit()
            session.refresh(user_roles, ["roles"])
            self.assertEqual(len(user_roles.roles), 1)
            self.assertEqual(user_roles.username, "user1")
            self.assertTrue(user_roles.roles[0].enabled)

    def test_create_without_repository(self):
        user_1 = self.user1
        roles = self.admin_role
        with Session(self.engine) as session:
            user_1 = self.account_repository.find_by_username(user_1.username, session=session)
            roles = [AccountRole(account_id=user_1.id, role_id=roles.id)]
            user_1.roles = roles
            session.commit()
            session.refresh(user_1, ["roles"])
        self.assertEqual(len(user_1.roles), 1)

    def test_create_with_repository(self):
        account_role = self.account_role_repository.create(self.user1, [self.user_role.id])
        self.assertEqual(len(account_role), 1)
        account_roles = self.account_role_repository.create(self.user2, [self.admin_role, self.user_role])
        self.assertEqual(len(account_roles), 2)

    def test_delete_user(self):
        account_role = self.account_role_repository.create(self.user1, self.user_role.id)
        self.account_role_repository.create(self.user2, self.user_role.id)
        self.assertEqual(len(account_role), 1)
        with Session(self.engine) as session:
            user_roles: Account = self.account_repository.find_by_id(self.user1.id, session=session)
            self.assertEqual(len(user_roles.roles), 1)
            session.delete(user_roles)
            session.commit()
        user_roles = self.role_repository.get(self.user_role.role)
        self.assertIsNotNone(user_roles)
        with Session(self.engine) as session:
            statement = select(AccountRole)
            account_roles = session.exec(statement).all()
            self.assertEqual(len(account_roles), 1)
            statement = select(Permission)
            permissions = session.exec(statement).all()
            self.assertEqual(len(permissions), 4)
            statement = select(Account)
            accounts = session.exec(statement).all()
            self.assertEqual(len(accounts), 1)

    def test_delete_role(self):
        account_role = self.account_role_repository.create(self.user1, [self.user_role.id, self.admin_role.id])
        self.account_role_repository.create(self.user2, self.user_role.id)
        self.assertEqual(len(account_role), 2)
        with Session(self.engine) as session:
            account_admin_role = self.account_role_repository.get(self.user1.id, self.user_role, session=session)
            session.delete(account_admin_role)
            session.commit()
        with Session(self.engine) as session:
            statement = select(Permission)
            permissions = session.exec(statement).all()
            self.assertEqual(len(permissions), 4)
            statement = select(Role)
            roles = session.exec(statement).all()
            self.assertEqual(len(roles), 2)

        role = self.role_repository.get(self.user_role.role)
        self.assertIsNotNone(role)
        user = self.account_repository.find_by_id(self.user1.id)
        self.assertIsNotNone(user)
        with Session(self.engine) as session:
            account_admin_role = self.account_role_repository.get(user, role, session=session)
            self.assertIsNone(account_admin_role)

    def test_get_refreshed(self):
        self.account_role_repository.create(self.user2, self.user_role.id)
        stored_account_role = self.account_role_repository.get_refreshed(Account(id=self.user2.id),
                                                                         Role(id=self.user_role.id))
        self.assertIsNotNone(stored_account_role)
        self.assertEqual(stored_account_role.account, self.user2)
        self.account_repository.delete(stored_account_role.account)
        stored_account_role = self.account_role_repository.get_refreshed(Account(id=self.user2.id),
                                                                         Role(id=self.user_role.id))
        self.assertIsNone(stored_account_role)
        user_role = self.role_repository.get(self.user_role.role)
        self.assertIsNotNone(user_role)
