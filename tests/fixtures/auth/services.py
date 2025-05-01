import pytest

@pytest.fixture
def mock_auth_service(fake_auth_repository, fake_banned_refresh_token_repository):
    from src.core.services.auth import AuthService

    return AuthService(
            auth_repository=fake_auth_repository, 
            banned_refresh_token_repository=fake_banned_refresh_token_repository
        )



@pytest.fixture
def auth_service(get_db_session, fake_banned_refresh_token_repository):
    from src.core.services.auth import AuthService
    from src.infrastructure.repositories import AuthRepository, BannedRefreshTokenRepository

    return AuthService(
            auth_repository=AuthRepository(session=get_db_session), 
            banned_refresh_token_repository=BannedRefreshTokenRepository(session=get_db_session)
        )