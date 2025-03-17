from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from sqlalchemy.future import select
from app.models.post import Post
from sqlalchemy.future import select


class PostRepository:
    """
    Repository for post-related database operations.
    """

    def __init__(self, db: AsyncSession):
        """
        Initialize repository with database session.
        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """
        Get post by ID.
        Args:
            post_id (int): Post ID
        Returns:
            Optional[Post]: Post object or None if not found
        """
        stmt = select(Post).where(Post.id==post_id)
        post = await self.db.execute(stmt)
        return post.scalars().first()

    async def get_by_user_id(self, user_id: int) -> List[Post]:
        """
        Get all posts by user ID.
        Args:
            user_id (int): User ID
        Returns:
            List[Post]: List of user's posts
        """
        stmt = select(Post).where(Post.user_id == user_id)
        post = await self.db.execute(stmt)
        return post.scalars().all()

    async def create(self, text: str, user_id: int) -> Post:
        """
        Create a new post.
        Args:
            text (str): Post text
            user_id (int): User ID
        Returns:
            Post: Created post object
        """
        db_post = Post(text=text, user_id=user_id)

        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post

    async def delete(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post by ID if it belongs to the user.
        Args:
            post_id (int): Post ID
            user_id (int): User ID
        Returns:
            bool: True if deleted, False if not found or not owned by user
        """
        stmt = select(Post).filter(
            Post.id == post_id,
            Post.user_id == user_id
        )
        result = await self.db.execute(stmt)
        db_post = result.scalars().first()
        if not db_post:
            return False

        await self.db.delete(db_post)
        await self.db.commit()
        return True
