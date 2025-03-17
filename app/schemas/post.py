from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    """Base schema for post data"""
    text: str = Field(..., description="Post content")

    @field_validator('text')
    def text_not_empty(cls, v):
        """Validate that text is not empty"""
        if not v.strip():
            raise ValueError('Post text cannot be empty')
        return v


class PostCreate(PostBase):
    """Schema for post creation"""
    pass


class PostInDB(PostBase):
    """Schema for post in database"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostResponse(PostBase):
    """Schema for post response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostIDResponse(BaseModel):
    """Schema for post ID response"""
    post_id: int = Field(..., description="ID of the created post")


class PostsResponse(BaseModel):
    """Schema for multiple posts response"""
    posts: List[PostResponse] = Field(..., description="List of posts")
