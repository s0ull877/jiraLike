from abc import ABC, abstractmethod
from uuid import UUID
from core.entities import User
from core.entities.auth import EmailVerification


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
    async def get_user(self, **fields) -> User:
        """
        Get a user by fields.
        
        class User:
            email: str
            password: str
            id: UUID | None 
            name: str 
            surname: str 
            is_active: bool 
            created_at: datetime 
            updated_at: datetime 
            timezone: str 
            image: str 
        """
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user: User) -> User:
        """
        Update an existing user.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def get_email_verification(self, code: UUID) -> EmailVerification | None:
        """
        Create a verification code for a user.
        """
        raise NotImplementedError
    
    @abstractmethod
    async def create_email_verification(self, email: str) -> EmailVerification | None:
        """
        Create a verification code for a user.
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