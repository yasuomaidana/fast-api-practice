from sqlalchemy import Engine
from sqlmodel import Session, select

from models import Permission
from models.security.permission.permission_type import PermissionType
from repository.utils import create_entity, with_session
from settings import engine


class PermissionRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(PermissionRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    def create(self, permission: Permission | PermissionType, session: Session = None):
        if isinstance(permission, PermissionType):
            permission = Permission(permission=permission)
        self._create(permission, session=session)
        return permission

    @create_entity
    def _create(self, permission: Permission, session: Session = None):
        return session.add(permission)

    @with_session
    def get(self, permission_type: PermissionType, session: Session=None) -> Permission | None:
        statement = select(Permission).where(Permission.permission == permission_type)
        return session.exec(statement).first()
