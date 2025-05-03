
import pytest
from faker import Faker

from src.core.entities.auth import User
from src.core.services.auth import AuthService

pytestmark = pytest.mark.asyncio

fake = Faker()

async def test_temp(auth_service):


    assert isinstance(auth_service, AuthService)

    user = User(
        email=fake.email(),
        password=fake.name()
    )
    db_user = await auth_service.create_user(user)

    assert db_user != None


async def test_login__failed(auth_service):

    email = fake.email()
    password = fake.name()

    user = User(
        email=email,
        password=password
    )
    db_user = await auth_service.create_user(user)
    
    assert db_user != None

    with pytest.raises(Exception) as exc_info:
        token = await auth_service.login(email, password)
    
    assert exc_info.value.args[0] == 'User email is not verified! Check email!'



async def test_login__success(auth_service):

    email = fake.email()
    password = fake.name()

    user = User(
        email=email,
        password=password
    )
    db_user = await auth_service.create_user(user)
    verification = await auth_service.create_verify_code(db_user)
    
    assert db_user != None
    assert verification != None

    activated_user = await auth_service.activate_user(code=verification.code, user=db_user)

    assert activated_user.is_active == True

    token = await auth_service.login(email, password)
    
    assert token != None
