from typing import Annotated

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2, OAuth2PasswordRequestForm
from starlette.status import HTTP_401_UNAUTHORIZED

from auth import AuthHandler
from settings import SecuritySettings


class OAuthProvider:
    _instance = None
    oauth2_scheme: OAuth2 = OAuth2PasswordBearer(tokenUrl=SecuritySettings().token_url)
    auth_handler: AuthHandler

    def __new__(cls, security_config: SecuritySettings = SecuritySettings(), auth_handler: AuthHandler = AuthHandler()):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.oauth2_scheme = OAuth2PasswordBearer(tokenUrl=security_config.token_url)
            cls._instance.auth_handler = auth_handler
            cls._instance.password_request_form = OAuth2PasswordRequestForm
        return cls._instance

    async def get_user(self, token: Annotated[str, oauth2_scheme]) -> str:
        user = self.auth_handler.decode_token(token)
        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
