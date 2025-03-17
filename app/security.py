from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional, Dict, Any

from app.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Args:
        plain_password (str): The plain text password
        hashed_password (str): The hashed password
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


async def get_password_hash(password: str) -> str:
    """
    Hash a password.
    Args:
        password (str): The plain text password
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


async def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    Args:
        data (Dict[str, Any]): Data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode a JWT token.
    Args:
        token (str): The token to decode
    Returns:
        Dict[str, Any]: The decoded token data
    Raises:
        JWTError: If token is invalid
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])