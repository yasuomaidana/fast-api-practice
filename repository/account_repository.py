from sqlalchemy import Engine
from sqlmodel import Session, select

from models import Account
from repository.utils import create_entity, with_session, transactional
from settings import engine


class AccountRepository:
    _instance = None

    def __new__(cls, _engine: Engine = engine):
        if cls._instance is None:
            cls._instance = super(AccountRepository, cls).__new__(cls)
            cls._instance.engine = _engine
        return cls._instance
    
    @create_entity
    def create(self, account: Account, session: Session = None):
        return session.add(account)
    
    @with_session
    def find_by_id(self, account_id: int, session: Session = None):
        return session.get(Account, account_id)
    
    @with_session
    def find_by_username(self, username: str, session: Session = None) -> Account | None:
        return session.exec(select(Account).where(Account.username == username)).first()
    
    @transactional
    def delete(self, account: Account, session: Session = None):
        return session.delete(account)