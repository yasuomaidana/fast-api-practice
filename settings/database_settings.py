from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    type: str = "sqlite"
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""
    
    @property
    def dsn(self):
        if self.type == "sqlite":
            return f"{self.type}:///{self.host}"
        auth = f"{self.user}:{self.password}@" if self.user and self.password else ""
        return f"{self.type}://{auth}{self.host}:{self.port}"
    

    model_config = SettingsConfigDict(env_prefix='database_')

database_settings = DatabaseSettings()