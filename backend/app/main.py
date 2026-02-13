from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
import traceback
import logging

# Load environment variables from .env file
load_dotenv()

from .api.health import router as health_router
from .api.todos import router as todos_router
from .api.auth import router as auth_router
from .database.session import create_db_and_tables

app = FastAPI(
    title="Todo API",
    description="API for managing todos in the Evolution of Todo - Phase II project",
    version="1.0.0"
)

# Configure CORS for Next.js frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers under /api/v1 prefix
app.include_router(health_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(todos_router, prefix="/api/v1")

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root route
@app.get("/")
def read_root():
    return JSONResponse(content={"message": "Welcome to the Todo API", "status": "running"}, status_code=200)

# Health check route
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "healthy", "message": "Todo API is running"}, status_code=200)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full error with traceback for debugging
    logging.error(f"Global exception: {exc}", exc_info=True)

    # Return a user-friendly error message
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred",
            "message": "Server error. Please try again later."
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)