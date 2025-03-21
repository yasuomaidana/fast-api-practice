from pydantic_settings import BaseSettings, SettingsConfigDict

from .algorithms import AlgorithmEnum


class SecuritySettings(BaseSettings):
    secret_key: str = "🤫it's a secret"
    algorithm: AlgorithmEnum = AlgorithmEnum.HS256
    expires_in: int = 3600  # seconds
    token_url: str = "/auth/oauth/token"

    model_config = SettingsConfigDict(env_prefix='security_')