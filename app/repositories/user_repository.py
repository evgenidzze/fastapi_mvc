from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.models.user import User
from app.security import get_password_hash, verify_password
from sqlalchemy.future import select


class UserRepository:
    """
    Repository for user-related database operations, including retrieving, creating, and verifying users.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize the repository with a SQLAlchemy database session.

        Args:
            db (Session): An active SQLAlchemy database session.
        """
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user from the database by their unique ID.

        Args:
            user_id (int): The unique identifier of the user.

        Returns:
            Optional[User]: A User object if found, otherwise None.
        """
        stmt = select(User).where(User.id==user_id)
        user = await self.db.execute(stmt)
        return user.scalars().first()

    async def get_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user from the database by their email address.

        Args:
            email (str): The email address of the user.

        Returns:
            Optional[User]: A User object if found, otherwise None.
        """
        stmt = select(User).where(User.email == email)
        user = await self.db.execute(stmt)
        return user.scalars().first()

    async def create(self, email: str, password: str) -> User:
        """
        Create a new user in the database with a hashed password.

        Args:
            email (str): The email address of the new user.
            password (str): The plain-text password to be hashed and stored.

        Returns:
            User: The created User object with an assigned ID and hashed password.

        Raises:
            IntegrityError: If a user with the given email already exists.
        """
        hashed_password = await get_password_hash(password)
        db_user = User(
            email=email,
            hashed_password=hashed_password
        )

        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def verify_credentials(self, email: str, password: str) -> Optional[User]:
        """
        Verify a user's credentials by checking the provided password against the stored hashed password.

        Args:
            email (str): The email address of the user attempting to authenticate.
            password (str): The plain-text password provided by the user.

        Returns:
            Optional[User]: The User object if authentication is successful, otherwise None.
        """
        user = await self.get_by_email(email)

        if not user:
            return None
        if not await verify_password(password, user.hashed_password):
            return None
        return user
