import datetime
import jwt
import pytest
from uuid import uuid4

from src.settings import get_settings

settings = get_settings()

pytestmark = pytest.mark.asyncio

async def test_temp(mock_auth_service):
    from src.core.services.auth import AuthService

    assert isinstance(mock_auth_service, AuthService)  


async def test_generate_access_token__success(mock_auth_service):

    data = {
        "sub": str(1),
    }

    access_token = mock_auth_service.create_access_token(data).token
    decoded_access_token = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
    decoded_token_expire = datetime.datetime.fromtimestamp(decoded_access_token.get("exp"), tz=datetime.timezone.utc)

    current_time = datetime.datetime.now(tz=datetime.UTC)

    assert (decoded_token_expire - current_time) > datetime.timedelta(minutes=settings.access_token_expire_minutes - 1)
    assert decoded_access_token['sub'] == data['sub']


async def test_generate_refresh_token__success(mock_auth_service):

    data = {
        "sub": str(1), "jti": str(uuid4())
    }

    refresh_token = mock_auth_service.create_refresh_token(data).token
    decoded_refresh_token = jwt.decode(refresh_token, settings.secret_key, algorithms=[settings.algorithm])
    decoded_token_expire = datetime.datetime.fromtimestamp(decoded_refresh_token.get("exp"), tz=datetime.timezone.utc)

    refresh_token_expire_minutes = settings.refresh_token_expire_days * 24 * 60
    current_time = datetime.datetime.now(tz=datetime.UTC)

    assert (decoded_token_expire - current_time) > datetime.timedelta(minutes=refresh_token_expire_minutes - 1)
    assert decoded_refresh_token['sub'] == data['sub']