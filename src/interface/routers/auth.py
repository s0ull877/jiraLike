import math
from fastapi import (
    APIRouter, Depends, Request, 
    Response, HTTPException, status
)
from core.entities.auth import Token, User
from core.services import AuthService, MailService
from interface.dependencies import get_auth_service, get_mail_service
from interface.schemas.auth import UserLogin, UserCreate, UserResponse
from settings import get_settings

settings = get_settings()

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
    mail_service: MailService = Depends(get_mail_service)
) -> UserResponse:
    """
    Create a new user.
    """
    user = User(**user.model_dump())
    
    user = await auth_service.create_user(user)
    email_verification = await auth_service.create_verify_code(user)
    await mail_service.send_verify_code(to=email_verification.email, code=email_verification.code)

    return UserResponse.model_validate(user)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    user_login: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Login a user and return a JWT token.
    """
    token: Token = await auth_service.login(user_login.email, user_login.password)

    response.set_cookie(
        key="access_token",
        value=token.access_token.token,
        httponly=True,
        secure=False if settings.is_debug_mode else True,
        samesite="Lax",
        max_age=math.ceil(token.access_token.expires.total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token.token,
        httponly=True,
        secure=False if settings.is_debug_mode else True,
        samesite="Lax",
        max_age=math.ceil(token.refresh_token.expires.total_seconds()),
    )
    return 


@router.get("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Logout a user
    """
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if refresh_token:
        await auth_service.logout(refresh_token)
        response.delete_cookie(key="refresh_token")

    if access_token:
        response.delete_cookie(key="access_token")

    return


@router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(
    request: Request,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    """
    Refresh a user's JWT token.
    """
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found",
        )
    
    token: Token = await auth_service.refresh(refresh_token)

    response.set_cookie(
        key="access_token",
        value=token.access_token.token,
        httponly=True,
        secure=False if settings.is_debug_mode else True,
        samesite="Lax",
        max_age=math.ceil(token.access_token.expires.total_seconds()),
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token.token,
        httponly=True,
        secure=False if settings.is_debug_mode else True,
        samesite="Lax",
        max_age=math.ceil(token.refresh_token.expires.total_seconds()),
    )

    return