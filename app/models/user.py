from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, mapped_column, Mapped

from app.models import Base


class User(Base):
    """
    SQLAlchemy model for users.

    Attributes:
        id (int): Primary key
        email (str): User email, unique
        hashed_password (str): Hashed password
        is_active (bool): User account status
        created_at (datetime): Account creation timestamp
        updated_at (datetime): Last update timestamp
        posts (relationship): Relationship to Post model
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Relationship with Post model
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
