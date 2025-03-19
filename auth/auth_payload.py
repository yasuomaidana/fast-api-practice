from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, Field

from settings.security import SecuritySettings


class AuthPayload(BaseModel):
    sub: str  # user id # user id
    """
    Using UTC for JWT authentication ensures that the token's expiration and issuance times are consistent and 
    not affected by time zone differences. 
    This avoids potential issues with token validation across different time zones, 
    ensuring that the tokens are valid and secure regardless of the user's location.
    """
    exp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(
        seconds=SecuritySettings().expires_in))  # expires in
    iat: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # issued at
