from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.controllers import auth_controller, post_controller
from app.config import settings
from app.models import Base, engine


app = FastAPI(
    title="Social Media API",
    description="A FastAPI social media application with user authentication and post management",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix=settings.API_PREFIX, tags=["Authentication"])
app.include_router(post_controller.router, prefix=settings.API_PREFIX, tags=["Posts"])


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request, exc):
    """
    Handles all SQLAlchemy exceptions.

    Args:
        request: The incoming request object.
        exc: The SQLAlchemy exception that was raised.

    Returns:
        JSONResponse: A response with status code 500 and a message about the database error.
    """
    return JSONResponse(
        status_code=500,
        content={"detail": "Database error occurred", "message": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
