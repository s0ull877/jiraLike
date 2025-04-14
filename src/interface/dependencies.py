import jwt
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.services import AuthService, MailService
from infrastructure.postgres_db import database
from infrastructure.broker.producer import broker_producer
from infrastructure.repositories import (
    AuthRepository,
    BannedRefreshTokenRepository,
)
from settings import get_settings

settings = get_settings()


async def get_auth_service(session: AsyncSession = Depends(database.get_db_session)):
    auth_repository = AuthRepository(session)
    token_repository = BannedRefreshTokenRepository(session)
    service = AuthService(auth_repository, token_repository)
    yield service


async def get_mail_service():
    service = MailService(broker_producer=broker_producer)
    yield service


class JWTBearer:

    async def __call__(self, request: Request):
        credentials = request.cookies.get("access_token")
        if credentials:
            try:
                payload = jwt.decode(
                    credentials, settings.secret_key, algorithms=[settings.algorithm]
                )
                request.state.payload = payload
                return payload
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Could not validate credentials",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="No credentials provided"
            )