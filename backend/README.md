# Todo Backend API

This is the backend API for the Evolution of Todo - Phase II project, built with FastAPI and SQLModel.

## Features

- RESTful API endpoints for Todo management
- PostgreSQL database with SQLModel ORM
- Complete CRUD operations for todos
- Health check endpoint

## Endpoints

### Health Check
- `GET /api/health` - Check API health status

### Todo Management
- `GET /api/todos` - Get all todos (with optional filtering and pagination)
- `GET /api/todos/{id}` - Get a specific todo
- `POST /api/todos` - Create a new todo
- `PUT /api/todos/{id}` - Update all fields of a todo
- `PATCH /api/todos/{id}` - Partially update a todo
- `DELETE /api/todos/{id}` - Delete a todo

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables (optional, defaults to SQLite):
```bash
export DATABASE_URL=postgresql://user:password@localhost/dbname
```

3. Run the application:
```bash
python -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.