from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List

from app.services.post_service import PostService
from app.schemas.post import PostCreate, PostResponse, PostIDResponse, PostsResponse
from dependencies import get_post_service, get_current_user_id, validate_payload_size

router = APIRouter(prefix="/posts")


@router.post("", response_model=PostIDResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(validate_payload_size)])
async def add_post(
        post_data: PostCreate,
        user_id: int = Depends(get_current_user_id),
        post_service: PostService = Depends(get_post_service)
):
    """
    Create a new post.
    Returns:
        PostIDResponse: Created post ID
    Raises:
        HTTPException: If user not found
    """
    try:
        post_id = await post_service.create_post(post_data.text, user_id)
        return post_id
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("", response_model=PostsResponse)
async def get_posts(
        user_id: int = Depends(get_current_user_id),
        post_service: PostService = Depends(get_post_service)
):
    """
    Get all posts by the authenticated user.
    Returns:
        PostsResponse: List of user's posts
    Raises:
        HTTPException: If user not found
    """
    try:
        posts = await post_service.get_user_posts(user_id)
        return PostsResponse(posts=posts)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
        post_id: int,
        user_id: int = Depends(get_current_user_id),
        post_service: PostService = Depends(get_post_service)
):
    """
    Delete a post by ID if it belongs to the authenticated user.
    Args:
        post_id (int): Post ID
        user_id (int): Current user ID from token
        post_service (PostService): Post service
    Returns:
        None
    Raises:
        HTTPException: If post not found or not owned by user
    """
    deleted = await post_service.delete_post(post_id, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found or not owned by user"
        )
    return None
