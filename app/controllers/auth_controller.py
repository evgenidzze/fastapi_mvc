from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.services.auth_service import AuthService
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from dependencies import get_auth_service

router = APIRouter(prefix="/auth")


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
        user_data: UserCreate,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Register a new user and return a JWT token.
    Args:
        user_data (UserCreate): User registration data
        auth_service (AuthService): Auth service
    Returns:
        TokenResponse: JWT token response
    Raises:
        HTTPException: If user with email already exists
    """
    try:
        token = await auth_service.register_user(user_data.email, user_data.password)
        return token
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(
        user_data: UserLogin,
        auth_service: AuthService = Depends(get_auth_service)
):
    """
    Authenticate user and return a token.
    Args:
        user_data (UserLogin): User login data
        auth_service (AuthService): Auth service
    Returns:
        TokenResponse: JWT token response
    Raises:
        HTTPException: If authentication fails
    """
    token = await auth_service.login_user(user_data.email, user_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    return token
