import pytest

class FakeAuthRepository:
    
    ...

@pytest.fixture  
def fake_auth_repository():

    return FakeAuthRepository()


class FakeannedRefreshTokenRepository:

   ...

@pytest.fixture  
def fake_banned_refresh_token_repository():

    return FakeannedRefreshTokenRepository()