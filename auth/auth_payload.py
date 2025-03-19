from datetime import datetime, timedelta

from pydantic import BaseModel

from settings.security import SecuritySettings


class AuthPayload(BaseModel):
    sub: int # user id
    exp: datetime = datetime.now() + timedelta(seconds=SecuritySettings().expires_in) # expires in
    iat: datetime = datetime.now() # issued at
