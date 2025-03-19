from pydantic_settings import BaseSettings, SettingsConfigDict

from .algorithms import AlgorithmEnum


class SecuritySettings(BaseSettings):
    secret_key: str = "🤫it's a secret"
    algorithm: str = AlgorithmEnum.HS256
    model_config = SettingsConfigDict(env_prefix='security_')
    expires_in: int = 3600 #seconds
