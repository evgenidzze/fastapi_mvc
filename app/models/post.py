from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models import Base


class Post(Base):
    """
    SQLAlchemy model for posts.

    Attributes:
        id (int): Primary key
        text (str): Post content
        user_id (int): Foreign key to users table
        created_at (datetime): Post creation timestamp
        updated_at (datetime): Last update timestamp
        author (relationship): Relationship to User model
    """
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationship with User model
    author = relationship("User", back_populates="posts")
