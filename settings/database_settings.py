from pydantic_settings import BaseSettings, SettingsConfigDict


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
            name = self.name.replace("_",".") if "_db" in self.name else self.name+".db"
            return f"{self.type}:///{name}"
        auth = f"{self.user}:{self.password}@" if self.user and self.password else ""
        return f"{self.type}://{auth}{self.host}:{self.port}/{self.name}"
    

    model_config = SettingsConfigDict(env_prefix='database_')

database_settings = DatabaseSettings()