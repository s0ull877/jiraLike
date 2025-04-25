import jwt
from dataclasses import dataclass
from uuid import UUID, uuid4
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from core.entities import User, AccessToken, RefreshToken, Token
from core.entities.auth import EmailVerification
from core.interfaceRepositories import (
    IAuthRepository, 
    IBannedRefreshTokenRepository,
)
from core.exceptions import (
    DuplicateEntryError,
    NotFoundError,
    InvalidCredentialsError,
)
from settings import get_settings


settings = get_settings()

@dataclass
class AuthService:
    
    def __init__(
        self,
        auth_repository: IAuthRepository,
        banned_refresh_token_repository: IBannedRefreshTokenRepository,
    ):
        
        self.auth_repository = auth_repository
        self.banned_refresh_token_repository = banned_refresh_token_repository
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


    async def create_user(self, user: User) -> User:
        """
        Create a new user.
        """

        if await self.auth_repository.get_user(email=user.email):
            raise DuplicateEntryError("User with this email already exists")
        
        user.password = self.pwd_context.hash(user.password)

        return await self.auth_repository.create_user(user)


    async def get_user(self, **fields) -> User:
        """
        Get a user by some fields.

        class User:
            id: UUID  
            email: str
            password: str
            name: str 
            surname: str 
            is_active: bool 
            created_at: datetime 
            updated_at: datetime 
            timezone: str 
            image: str | None
        """

        user: User | None = await self.auth_repository.get_user(**fields)

        return user


    async def update_user(self, user: User) -> User:
        """
        Update an existing user.
        """

        if not self.auth_repository.get_user(id=user.id):
            raise NotFoundError("User not found")
        
        user.password = self.pwd_context.hash(user.password)

        return await self.auth_repository.update_user(user)


    async def login(self, email: str, password: str) -> Token:
        """
        Login a user.
        """

        user = await self.get_user(email=email)

        if not user:
            raise NotFoundError("User not found")
        
        if not self.pwd_context.verify(password, user.password):
            raise NotFoundError("Invalid email or password")
        
        if not user.is_active:
            raise InvalidCredentialsError("User email is not verified! Check email!")
        
        access_token = self.create_access_token(
            {"sub": str(user.id)}
        )
        refresh_token = self.create_refresh_token(
            {"sub": str(user.id), "jti": str(uuid4())}
        )

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    async def logout(self, token: str) -> None:
        """
        Logout a user.
        """

        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        jti: str = payload.get("jti")

        banned_token = (
            await self.banned_refresh_token_repository.create_banned_refresh_token(
                jti=jti
            )
        )

        return banned_token
    

    async def create_verify_code(self, user: User) -> EmailVerification | None:
        """
        Create a verification code.
        """

        if await self.auth_repository.get_email_verification(email=user.email):
            raise DuplicateEntryError("Verification with this email already exists")
        
        email_verification = EmailVerification(
            code=uuid4(),
            email=user.email
        )
        return await self.auth_repository.create_email_verification(emailverification=email_verification)
    

    async def activate_user(self, code: str, user: User):

        email_verificatiion = await self.auth_repository.get_email_verification(email=user.email)

        if email_verificatiion is None:
            raise NotFoundError("Veriification not found")

        if email_verificatiion.code != UUID(code):
            raise NotFoundError("Verification not found")
        
        user.is_active = True
        
        updated_user = await self.auth_repository.update_user(user)

        if updated_user is None:
            raise Exception
        
        return user
        

        
        

    async def refresh(self, token: str) -> Token:
        """
        Refresh a user's JWT token.
        """

        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise NotFoundError("User not found")
       
        user = await self.auth_repository.get_user(id=UUID(user_id))
        if user is None:
            raise NotFoundError("User not found")
        
        jti = payload.get("jti")
        if jti is None:
            raise NotFoundError("Invalid token")
        
        banned_token = (
            await self.banned_refresh_token_repository.is_banned_refresh_token(jti=jti)
        )
        
        if banned_token:
            raise NotFoundError("Token is banned")
        
        await self.banned_refresh_token_repository.create_banned_refresh_token(jti=jti)
        
        access_token = self.create_access_token(
            {"sub": str(user.id)}
        )
        refresh_token = self.create_refresh_token(
            {"sub": str(user.id), "jti": str(uuid4())}
        )
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
        )


    def create_access_token(self, data: dict) -> AccessToken:

        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire, "type": "access"})

        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )

        return AccessToken(
            token=encoded_jwt,
            type="Bearer",
            expires=timedelta(minutes=settings.access_token_expire_minutes),
        )


    def create_refresh_token(self, data: dict) -> RefreshToken:

        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )
        to_encode.update({"exp": expire, "type": "refresh"})

        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )

        return RefreshToken(
            token=encoded_jwt,
            type="Bearer",
            expires=timedelta(days=settings.refresh_token_expire_days),
            jti=data["jti"],
        )


    async def verify_access_token(self, token: str) -> bool:

        try:

            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )

            if payload.get("type") != "access":
                return None
            
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            
            user = await self.auth_repository.get_user(id=UUID(user_id))
            if user is None:
                return None
            
            return True
        
        except jwt.PyJWTError:
            return None


    async def verify_refresh_token(self, token: str) -> bool:

        try:

            payload = jwt.decode(
                token, settings.secret_key, algorithms=[settings.algorithm]
            )

            if payload.get("type") != "refresh":
                return None
            
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            
            user = await self.auth_repository.get_user(id=UUID(user_id))
            if user is None:
                return None
            
            jti = payload.get("jti")
            if jti is None:
                return None
            
            banned_token = (
                await self.banned_refresh_token_repository.is_banned_refresh_token(
                    jti=jti
                )
            )
            if banned_token:
                return None
            
            return True
        
        except jwt.PyJWTError:
            return None
