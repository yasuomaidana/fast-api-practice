from functools import wraps

from sqlmodel import Session, SQLModel


def with_session(func):
    """
    Decorator to ensure a session is available for the decorated function.

    This decorator applies the following behaviors:
    - Checks if a session is provided in the function's keyword arguments.
    - If no session is provided, it creates a new session using the engine.
    - Passes the session to the decorated function.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with the applied behaviors.
    """

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
    """
    Decorator to handle transactions in the database.

    This decorator applies the following behaviors:
    - Ensures a session is available using the `with_session` decorator.
    - Commits the transaction after the function call.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with the applied behaviors.
    """

    @wraps(func)
    @with_session
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        kwargs['session'].commit()
        return result

    return wrapper


def refreshable(func) -> SQLModel:
    """
    Decorator to refresh an entity after a function call.

    This decorator applies the following behaviors:
    - Ensures the entity is refreshed after the function call.
    - Optionally refreshes specific attributes if `attribute_names` is provided.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with the applied behaviors.
    """

    @wraps(func)
    @with_session
    def wrapper(self, to_refresh: SQLModel, *args, attribute_names: list = None, **kwargs):
        func(self, to_refresh, *args, **kwargs)
        kwargs['session'].refresh(to_refresh, attribute_names=attribute_names)
        return to_refresh

    return wrapper


def refresh_output(func) -> SQLModel:
    @wraps(func)
    @with_session
    def wrapper(self, *args, attribute_names: list[str] = None, **kwargs):
        result = func(self, *args, **kwargs)
        if result is None:
            return None
        kwargs['session'].refresh(result, attribute_names=attribute_names)
        return result

    return wrapper


def create_entity(func):
    """
    Decorator to handle the creation of an entity in the database.

    This decorator applies the following behaviors:
    - Ensures a session is available using the `with_session` decorator.
    - Refreshes the entity after creation using the `refreshable` decorator.
    - Commits the transaction using the `transactional` decorator.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function with the applied behaviors.
    """

    @wraps(func)
    @refreshable
    @transactional
    def wrapper(self, to_store: SQLModel, session: Session = None):
        func(self, to_store, session=session)

    return wrapper


def ids_extractor(to_extract: int | SQLModel | list[int] | list[SQLModel]) -> list[int]:
    """
    Extracts the ids from the provided entities.

    Args:
        to_extract (int | SQLModel | list[int] | list[SQLModel]): The entity or entities to extract the ids from.

    Returns:
        list[int]: The extracted ids.
    """
    if isinstance(to_extract, list) and isinstance(to_extract[0], int):
        return to_extract
    if isinstance(to_extract, int):
        return [to_extract]
    if isinstance(to_extract, SQLModel):
        return [to_extract.id]
    return [entity.id for entity in to_extract]
