# Evolution of Todo – Phase II

This project represents Phase II of the Evolution of Todo application, transforming the original console-based Python application into a full-stack web application using Next.js, FastAPI, SQLModel, and Neon PostgreSQL.

## Architecture

The application follows a clean architecture with:
- **Frontend**: Next.js 14+ with App Router
- **Backend**: FastAPI for REST API
- **ORM**: SQLModel for unified data modeling
- **Database**: PostgreSQL (compatible with Neon)

## Features

- Complete Todo CRUD operations
- Persistent storage with PostgreSQL
- Responsive web interface
- RESTful API design
- Type-safe frontend and backend

## Project Structure

```
├── backend/           # FastAPI backend application
│   ├── app/          # Application code
│   ├── requirements.txt
│   └── README.md
├── frontend/         # Next.js frontend application
│   ├── src/          # Source code
│   ├── package.json
│   └── README.md
└── .history/         # Project specifications and artifacts
    ├── constitution.md
    └── phase2/
        ├── specs/
        ├── tasks/
        └── plans/
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the backend server:
```bash
python -m uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

The backend exposes the following API endpoints:

- `GET /api/health` - Health check
- `GET /api/todos` - Get all todos
- `GET /api/todos/{id}` - Get specific todo
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `PATCH /api/todos/{id}` - Partial update of todo
- `DELETE /api/todos/{id}` - Delete todo

## Development

For development, both applications should be running simultaneously:
- Backend on `http://localhost:8000`
- Frontend on `http://localhost:3000`

The frontend expects the backend API to be available at `/api` relative to the frontend URL, which is configured in the `.env.local` file. 
"# todo-app-phase-2" 
"# todo-app-phase-2" 
