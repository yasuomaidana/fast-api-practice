from functools import wraps

from sqlmodel import Session


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