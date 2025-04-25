import pytest
from src.core.services.auth import AuthService

@pytest.fixture
def mock_auth_service(fake_auth_repository, fake_banned_refresh_token_repository) -> AuthService:

    return AuthService(
            auth_repository=fake_auth_repository, 
            banned_refresh_token_repository=fake_banned_refresh_token_repository
        )