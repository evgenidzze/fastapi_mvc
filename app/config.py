from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = "user"
    MYSQL_ROOT_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_NAME: str = "social_media_db"

    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "your-secret-key-for-jwt"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CACHE_EXPIRY: int = 300  # 5 minutes in seconds

    MAX_PAYLOAD_SIZE: int = 1048576  # 1 MB in bytes

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        """
        Constructs the full database connection string from individual components.
        """
        return f"mysql+aiomysql://{self.DB_USER}:{self.MYSQL_ROOT_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


settings = Settings()