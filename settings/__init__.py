from sqlmodel import create_engine

from .database_settings import DatabaseSettings
from .security import SecuritySettings

database_settings = DatabaseSettings()
security_settings = SecuritySettings()
engine = create_engine(database_settings.dsn, echo=True)
