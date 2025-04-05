from abc import ABC, abstractmethod
from uuid import UUID
from core.entities import User


class IAuthRepository(ABC):
    """
    Interface for the authentication repository.
    """

    @abstractmethod
    async def create_user(self, user: User) -> User:
        """
        Create a new user.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: str) -> User:
        """
        Get a user by ID.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """
        Update an existing user.
        """
        raise NotImplementedError


class IBannedRefreshTokenRepository(ABC):
    """
    Interface for the banned refresh token repository.
    """

    @abstractmethod
    async def create_banned_refresh_token(self, jti: UUID) -> None:
        """
        Create a new banned refresh token.
        """
        raise NotImplementedError

    @abstractmethod
    async def is_banned_refresh_token(self, jti: UUID) -> bool:
        """
        Check if a refresh token is banned.
        """
        raise NotImplementedError