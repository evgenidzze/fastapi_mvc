# FastAPI Social Media API

A RESTful API for a social media application built with FastAPI, SQLAlchemy ORM, and MySQL. This project follows the MVC
architecture pattern with separate layers for routing, business logic, and database operations.

## Project Structure

```
app/

├── controllers/    # Controllers/Routes layer
├── services/       # Business logic layer
├── repositories/   # Data access layer
├── models/         # Database models
└── schemas/        # Pydantic schemas
```

## API Endpoints

### Authentication Endpoints

- `POST /api/v1/auth/signup`: Register a new user
- `POST /api/v1/auth/login`: Authenticate a user and receive a token

### Post Endpoints

- `POST /api/v1/posts`: Create a new post
- `GET /api/v1/posts`: Get all posts for the authenticated user
- `DELETE /api/v1/posts/{post_id}`: Delete a post

## Running the Application

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DB_USER=your_db_user
MYSQL_ROOT_PASSWORD=your_db_password
DB_HOST=localhost
DB_NAME=social_media_db
SECRET_KEY=your_secret_key_for_jwt
```

### Method 1: Running Locally

#### Prerequisites:

- Python 3.12+
- MySQL database
- [Optional] Docker and Docker Compose

1. Clone repository:
   ```
   https://github.com/evgenidzze/fastapi_mvc
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at `http://localhost:8000/docs`

### Method 2: Running with Docker Compose

Run with Docker Compose:

1. Clone repository:
   ```
   https://github.com/evgenidzze/fastapi_mvc
   ```

2. Run docker compose
   ```bash
   docker compose up -d --build
   ```