from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import NotFoundError
from core.entities import User, EmailVerification
from core.interfaceRepositories import IAuthRepository, IBannedRefreshTokenRepository

from infrastructure.models import (
    User as UserModel, 
    BannedRefreshToken as BannedRefreshTokenModel,
    EmailVerification as EmailVerificationModel
)


class AuthRepository(IAuthRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_user(self, user_model: UserModel) -> User:
        
        return User(
            id=user_model.id,
            email=user_model.email,
            password=user_model.password,
            name=user_model.name,
            surname=user_model.surname,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            timezone=user_model.timezone,
            image=user_model.image,
        )


    async def get_user(self, **fields) -> User | None:
        """
        Get a user by fields.
        
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
        try:

            stmt = select(UserModel).filter_by(**fields)
            result = await self.session.execute(stmt)
            user = result.scalars().first()

            if not user:
                return None
            
            return self._to_user(user)
        
        except Exception as e:
            print(f"Error getting user: {e}")
            return None


    async def create_user(self, user: User) -> User:
        """
        Create a new user.

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
        try:

            user_model = UserModel(
                email=user.email,
                password=user.password,
                name=user.name,
                surname=user.surname,
                is_active=user.is_active,
                timezone=user.timezone,
                image=user.image,
            )

            self.session.add(user_model)

            await self.session.commit()
            await self.session.refresh(user_model)

            return self._to_user(user_model)
        
        except Exception as e:
            print(f"Error creating user: {e}")
            return None


    async def update_user(self, user: User) -> User:
        """
        Update an existing user.

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
        try:

            stmt = select(UserModel).filter_by(id=user.id)
            result = await self.session.execute(stmt)
            user_model = result.scalars().first()

            if not user_model:
                raise NotFoundError(f"User with ID {user.id} not found")

            user_model.email = user.email
            user_model.password = user.password
            user_model.name = user.name
            user_model.surname = user.surname
            user_model.is_active = user.is_active
            user_model.timezone=user.timezone
            user_model.image=user.image

            await self.session.commit()
            await self.session.refresh(user_model)

            return self._to_user(user_model)
        
        except NotFoundError:
            raise

        except Exception as e:
            print(f"Error updating user: {e}")
            return None



    async def get_email_verification(self, email: str) -> EmailVerification | None:

        try:

            stmt = select(EmailVerificationModel).filter_by(email=email)
            result = await self.session.execute(stmt)
            emailverification_model = result.scalars().first()

            if not emailverification_model:
                return None
            
            return EmailVerification(
                code=emailverification_model.code,
                email=emailverification_model.email,
            )
        
        except Exception as e:
            print(f"Error getting email verification: {e}")
            return None



    async def create_email_verification(self, emailverification: EmailVerification) -> EmailVerification | None:

        try:

            emailverification_model = EmailVerificationModel(
                email=emailverification.email,
                code=emailverification.code,
            )

            self.session.add(emailverification_model)

            await self.session.commit()
            await self.session.refresh(emailverification_model)

            return EmailVerification(
                code=emailverification_model.code,
                email=emailverification_model.email,
            )
        
        except Exception as e:
            print(f"Error creating email verification: {e}")
            return None


    


class BannedRefreshTokenRepository(IBannedRefreshTokenRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_banned_refresh_token(self, jti: UUID) -> None:
        """
        Create a banned refresh token.
        """
        try:

            banned_token = BannedRefreshTokenModel(
                jti=str(jti),
            )

            self.session.add(banned_token)

            await self.session.commit()
            await self.session.refresh(banned_token)


        except Exception as e:
            print(f"Error creating user: {e}")
            return None


    async def is_banned_refresh_token(self, jti: UUID) -> bool:
        """
        Check the refresh token is banned.
        """
        stmt = select(BannedRefreshTokenModel).filter_by(jti=str(jti))
        result = await self.session.execute(stmt)
        banned_token = result.scalars().first()

        if banned_token:
            return True
        
        return False