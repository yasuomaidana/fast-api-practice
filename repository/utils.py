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
            return result
        return func(self, *args, **kwargs)

    return wrapper


def transactional(func):
    @wraps(func)
    @with_session
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        kwargs['session'].commit()
        return result

    return wrapper


def refreshable(func):
    @wraps(func)
    def wrapper(self, to_refresh: SQLModel, *args, attribute_names: list = None, **kwargs):
        func(self, to_refresh, *args, **kwargs)
        kwargs['session'].refresh(to_refresh, attribute_names=attribute_names)
        return to_refresh

    return wrapper


def create_entity(func):
    @wraps(func)
    @with_session
    @refreshable
    @transactional
    def wrapper(self, to_store: SQLModel, session: Session = None):
        func(self, to_store, session=session)

    return wrapper
