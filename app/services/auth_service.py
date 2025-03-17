from datetime import timedelta
from typing import Optional

from app.config import settings
from app.repositories.user_repository import UserRepository
from app.security import create_access_token
from app.schemas.auth import TokenResponse


class AuthService:
    """
    Service for authentication business logic.
    """

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, email: str, password: str) -> TokenResponse:

        existing_user = await self.repository.get_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")

        user = await self.repository.create(email, password)

        access_token = await create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(access_token=access_token)

    async def login_user(self, email: str, password: str) -> Optional[TokenResponse]:
        user = await self.repository.verify_credentials(email, password)
        if not user:
            return None

        access_token = await create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return TokenResponse(access_token=access_token)