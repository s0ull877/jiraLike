from uuid import UUID
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from infrastructure.models.base import BaseModelMixin
from infrastructure.postgres_db import Base
import pytz


class BannedRefreshToken(Base, BaseModelMixin):
    __tablename__ = "BannedRefreshTokens"

    jti: Mapped[str] = mapped_column(nullable=False, unique=True)


class User(Base, BaseModelMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    surname: Mapped[str] = mapped_column(String(80), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=False)
    timezone: Mapped[str] = mapped_column(default=str(pytz.timezone("Europe/Moscow")))
    image: Mapped[str] = mapped_column(nullable=True)



class EmailVerification(Base, BaseModelMixin):
    __tablename__ = "email_verifications"

    code: Mapped[UUID] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(80), nullable=False, unique=True)