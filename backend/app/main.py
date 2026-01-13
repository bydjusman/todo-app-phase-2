from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Include API routers under /api prefix
app.include_router(health_router, prefix="/api")
app.include_router(todos_router, prefix="/api")
app.include_router(auth_router, prefix="/api")

# Create database tables on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)