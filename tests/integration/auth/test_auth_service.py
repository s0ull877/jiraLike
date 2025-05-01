
import pytest
from sqlalchemy import select, insert

from src.core.entities.auth import User
from src.core.services.auth import AuthService

pytestmark = pytest.mark.asyncio


async def test_temp(auth_service):


    assert isinstance(auth_service, AuthService)

    user = User(
        email="somsadsemail@mail.com",
        password="somepassword"
    )
    db_user = await auth_service.create_user(user)

    print(f'\nUSER: {db_user}\n')
    assert db_user != None