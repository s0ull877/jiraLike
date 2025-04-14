from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from uuid import UUID
from typing import List


class UserBase(BaseModel):
    email: EmailStr
    name: str = Field(..., min_length=3)
    surname: str = Field(..., min_length=3)


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator("password")
    def password_strength(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.islower() for char in v):
            raise ValueError("Password must contain at least one lowercase letter")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: UUID
    email: EmailStr
    name: str
    surname: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    image: str | None
    timezone: str

    class Config:
        from_attributes = True