from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlmodel import create_engine


class DatabaseSettings(BaseSettings):
    type: str = "sqlite"
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""
    name: str = "testing_db"

    @property
    def dsn(self):
        if self.type == "sqlite":
            name = self.name.replace("_", ".") if "_db" in self.name else self.name
            return f"{self.type}:///{name}"
        auth = f"{self.user}:{self.password}@" if self.user and self.password else ""
        return f"{self.type}://{auth}{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(env_prefix='database_')


database_settings = DatabaseSettings()

print(f"Database settings: \t{database_settings.model_dump(mode="json")}")
print("Database DSN: \t", database_settings.dsn)
engine = create_engine(database_settings.dsn, echo=True)
