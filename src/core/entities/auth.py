import pytz
from uuid import UUID
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from settings import get_settings

settings = get_settings()


@dataclass
class User:
    """
    User entity class.
    """

    email: str
    password: str
    id: UUID | None = field(default=None)
    name: str = field(default="")
    surname: str = field(default="")
    is_active: bool = field(default=True)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    timezone: str = field(default=str(pytz.timezone("Europe/Moscow")))
    image: str = field(default="")


@dataclass
class AccessToken:
    token: str
    type: str = field(default="Bearer")
    expires: timedelta = field(default_factory=lambda: timedelta(minutes=settings.accss_token_expire_minutes)) 


@dataclass
class RefreshToken:
    token: str
    type: str = field(default="Bearer")
    expires: timedelta = field(default_factory=lambda: timedelta(days=settings.refresh_token_expire_days)) 
    jti: UUID = field(default="")


@dataclass
class Token:
    """
    Token entity class.
    """

    access_token: AccessToken
    refresh_token: RefreshToken


@dataclass
class BannedRefreshToken:
    """ "
    Banned refresh token entity class.
    """

    jti: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
