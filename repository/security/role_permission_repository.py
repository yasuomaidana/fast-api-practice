from sqlalchemy import Engine
from sqlmodel import Session, select

from models import RolePermission, Role, Permission
from repository.utils import create_entity, with_session
from settings import engine


class RolePermissionRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(RolePermissionRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    def create(self, role: int | Role, permission: int | Permission, session: Session = None):
        role_id = role if isinstance(role, int) else role.id
        permission_id = permission if isinstance(permission, int) else permission.id
        
        role_permission = RolePermission(role_id=role_id, permission_id=permission_id)
        self._create(role_permission, session=session)
        return role_permission

    @create_entity
    def _create(self, role_permission: RolePermission, session: Session = None):
        return session.add(role_permission)

    def get(self, role: int | Role, permission: int | Permission, session: Session = None) -> RolePermission | None:
        role_id = role if isinstance(role, int) else role.id
        permission_id = permission if isinstance(permission, int) else permission.id

        return self._get(role_id, permission_id, session=session)

    @with_session
    def _get(self, role_id: int, permission_id: int, session: Session = None) -> RolePermission | None:
        statement = select(RolePermission).where(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        )
        return session.exec(statement).one_or_none()
