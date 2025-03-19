from functools import wraps

from sqlmodel import Session, SQLModel


def with_session(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session is None:
            with Session(self.engine) as session:
                kwargs['session'] = session
                result = func(self, *args, **kwargs)
            session.close()
            return result
        return func(self, *args, **kwargs)

    return wrapper


def transactional(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        session = kwargs.get('session', None)
        if session is None:
            with Session(self.engine) as session:
                kwargs['session'] = session
                result = func(self, *args, **kwargs)
                session.commit()
            session.close()
            return result

    return wrapper


def create_entity(func):
    @wraps(func)
    def wrapper(self, to_store: SQLModel, session: Session = None):
        if session is None:
            with Session(self.engine) as session:
                session.add(to_store)
                session.commit()
                session.refresh(to_store)
                session.close()
            return to_store
        func(self, to_store, session)

    return wrapper
