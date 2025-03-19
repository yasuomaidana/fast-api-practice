import jwt
from fastapi import HTTPException, Security

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext

from auth.auth_payload import AuthPayload
from settings.security.security_settings import SecuritySettings


class AuthHandler:
    _instance = None
    security = HTTPBearer()
    password_context = CryptContext(schemes=["bcrypt"])
    secret = SecuritySettings().secret_key
    algorithm = SecuritySettings().algorithm

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthHandler, cls).__new__(cls)
        return cls._instance

    def get_password_hash(self, password):
        return self.password_context.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_context.verify(plain_password, hashed_password)

    def encode_token(self, username:str):
        payload = AuthPayload(sub=username)
        return jwt.encode(dict(payload), self.secret, algorithm=self.algorithm)

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=[self.algorithm])
            return AuthPayload(**payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
