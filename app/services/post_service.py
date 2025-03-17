from typing import List, Optional

from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas.post import PostResponse, PostIDResponse
from app.models.post import Post
from app.cache import cache
from app.config import settings


class PostService:
    """
    Service for handling post-related business logic, including creation, retrieval, and deletion of posts.
    """

    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        """
        Initialize the PostService with the necessary repositories.
        Args:
            post_repository (PostRepository): Repository for post-related database operations.
            user_repository (UserRepository): Repository for user-related database operations.
        """
        self.post_repository = post_repository
        self.user_repository = user_repository

    async def create_post(self, text: str, user_id: int) -> PostIDResponse:
        """
        Create a new post for a given user.
        Args:
            text (str): The content of the post.
            user_id (int): The ID of the user creating the post.
        Returns:
            PostIDResponse: The ID of the created post.
        Raises:
            ValueError: If the user does not exist.
        """
        user = await self.user_repository.get_by_id(user_id)

        if not user:
            raise ValueError("User not found")

        post = await self.post_repository.create(text, user_id)
        await cache.delete_pattern(f"user_posts_{user_id}")
        return PostIDResponse(post_id=post.id)

    async def get_user_posts(self, user_id: int) -> List[PostResponse]:
        """
        Retrieve all posts created by a specific user.
        Args:
            user_id (int): The ID of the user whose posts are being retrieved.
        Returns:
            List[PostResponse]: A list of posts created by the user.
        Raises:
            ValueError: If the user does not exist.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        cache_key = f"user_posts_{user_id}"
        cached_posts = await cache.get(cache_key)
        if cached_posts:
            return cached_posts

        posts = await self.post_repository.get_by_user_id(user_id)
        response_posts = [PostResponse.from_orm(post) for post in posts]
        await cache.set(cache_key, response_posts, settings.CACHE_EXPIRY)

        return response_posts

    async def delete_post(self, post_id: int, user_id: int) -> bool:
        """
        Delete a post created by a specific user.

        Args:
            post_id (int): The ID of the post to be deleted.
            user_id (int): The ID of the user requesting the deletion.

        Returns:
            bool: True if the post was successfully deleted, False otherwise.
        """
        deleted = await self.post_repository.delete(post_id, user_id)
        if deleted:
            await cache.delete_pattern(f"user_posts_{user_id}")
        return deleted
