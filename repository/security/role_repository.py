from sqlalchemy import Engine
from sqlmodel import Session, select

from models import Role
from models.security.role.role_type import RoleType
from repository.utils import create_entity, with_session
from settings import engine


class RoleRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(RoleRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    def create(self, role: RoleType | Role, session: Session = None):
        if isinstance(role, RoleType):
            role = Role(role=role)
        self._create(role, session=session)
        return role

    @create_entity
    def _create(self, role: Role, session: Session = None):
        return session.add(role)

    @with_session
    def get(self, role_type: RoleType, session: Session = None):
        statement = select(Role).where(Role.role == role_type)
        return session.exec(statement).first()
