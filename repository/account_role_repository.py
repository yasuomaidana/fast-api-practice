from sqlalchemy import Engine
from sqlmodel import Session, select

from models import AccountRole, Account, Role
from repository.utils import create_entity, ids_extractor, with_session
from settings import engine


class AccountRoleRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(AccountRoleRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance

    def create(self, account: int | Account, role: int | Role | list[int] | list[Role], session: Session = None) -> \
            list[AccountRole]:
        account_id = account if isinstance(account, int) else account.id
        role_ids = ids_extractor(role)

        account_roles = [self._create(AccountRole(account_id=account_id, role_id=role_id), session=session) for role_id
                         in role_ids]

        return account_roles

    @create_entity
    def _create(self, account_role: AccountRole, session: Session = None):
        return session.add(account_role)

    def get(self, account: int | Account, role: int | Role, session: Session = None) -> AccountRole | None:
        account_id = account if isinstance(account, int) else account.id
        role_id = role if isinstance(role, int) else role.id
        return self._get(AccountRole(account_id=account_id, role_id=role_id), session=session)

    @with_session
    def _get(self, account_role: AccountRole, session: Session = None) -> AccountRole | None:
        statement = select(AccountRole).where(AccountRole.account_id == account_role.account_id).where(
            AccountRole.role_id == account_role.role_id)
        return session.exec(statement).first()
