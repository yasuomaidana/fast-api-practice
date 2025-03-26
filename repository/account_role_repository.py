from sqlalchemy import Engine
from sqlmodel import Session

from models import AccountRole, Account, Role
from repository.utils import create_entity, ids_extractor
from settings import engine


class AccountRoleRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(AccountRoleRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    def create(self, account: int | Account, role: int | Role | list[int] | list[Role], session: Session = None)->list[AccountRole]:
        account_id = account if isinstance(account, int) else account.id
        role_ids = ids_extractor(role)

        account_roles = [self._create(AccountRole(account_id=account_id, role_id=role_id), session=session) for role_id
                         in role_ids]

        return account_roles

    @create_entity
    def _create(self, account_role: AccountRole, session: Session = None):
        return session.add(account_role)
