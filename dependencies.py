
from fastapi import Depends, HTTPException, status, Header, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from typing import Optional, Dict, Any

from app.models import get_db
from app.security import decode_token
from app.config import settings
from app.repositories.user_repository import UserRepository
from app.repositories.post_repository import PostRepository
from app.services.auth_service import AuthService
from app.services.post_service import PostService

security = HTTPBearer()


# Repository dependencies
async def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Get user repository instance.
    Args:
        db (Session): Database session
    Returns:
        UserRepository: User repository instance
    """
    return UserRepository(db)


async def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    """
    Get post repository instance.
    Args:
        db (Session): Database session
    Returns:
        PostRepository: Post repository instance
    """
    return PostRepository(db)


# Service dependencies
async def get_auth_service(repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    """
    Get auth service instance.
    Args:
        repo (UserRepository): User repository
    Returns:
        AuthService: Auth service instance
    """
    return AuthService(repo)


async def get_post_service(
        post_repo: PostRepository = Depends(get_post_repository),
        user_repo: UserRepository = Depends(get_user_repository)
) -> PostService:
    """
    Get post service instance.
    Args:
        post_repo (PostRepository): Post repository
        user_repo (UserRepository): User repository
    Returns:
        PostService: Post service instance
    """
    return PostService(post_repo, user_repo)


async def get_token_data(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Get and validate token data.
    Args:
        credentials (HTTPAuthorizationCredentials): HTTP authorization credentials
    Returns:
        Dict[str, Any]: Token data
    Raises:
        HTTPException: If token is invalid
    """
    try:
        token = credentials.credentials
        payload = await decode_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id, "token": token}
    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user_id(token_data: Dict[str, Any] = Depends(get_token_data)) -> int:
    """
    Get current user ID from token data
    Args:
        token_data (Dict[str, Any]): Token data
    Returns:
        int: User ID
    """
    return int(token_data["user_id"])


async def validate_payload_size(request: Request):
    """
    Validate that request payload doesn't exceed maximum size.
    Args:
        request (Request): FastAPI request object
    Raises:
        HTTPException: If payload size exceeds maximum
    """
    content_length = request.headers.get("content-length")
    if content_length and int(content_length) > settings.MAX_PAYLOAD_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Payload too large. Maximum size is {settings.MAX_PAYLOAD_SIZE} bytes"
        )
