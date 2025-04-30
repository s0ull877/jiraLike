import pytest

@pytest.fixture
def mock_auth_service(fake_auth_repository, fake_banned_refresh_token_repository):
    from src.core.services.auth import AuthService

    return AuthService(
            auth_repository=fake_auth_repository, 
            banned_refresh_token_repository=fake_banned_refresh_token_repository
        )