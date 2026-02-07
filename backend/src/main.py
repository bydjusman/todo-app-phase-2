from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import src.models as models # Taake server start hote hi models register ho jayein

from config import settings
from models.database import async_engine
#from api import auth, tasks, categories_router
# Purani line (from api import auth...) ko delete karein aur ye likhein:
from api.auth import router as auth_router
from api.tasks import router as tasks_router
# Agar categories_router api folder ke andar kisi file mein hai (e.g. categories.py):
#from api.categories import router as categories_router
from src.api.tasks import router as categories_router

from api.exceptions import setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown events."""
    # Startup
    logger.info("Starting up Todo Backend API...")
    logger.info(f"Database URL: {settings.database_url[:50]}...")
    logger.info(f"Environment: {settings.environment}")

    yield

    # Shutdown
    logger.info("Shutting down Todo Backend API...")
    await async_engine.dispose()


# Create FastAPI application
app = FastAPI(
    title="Todo API",
    description="Full-stack Todo Application Backend",
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Setup exception handlers
setup_exception_handlers(app)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
#app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
#app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
#app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])


# In lines ko aise update karein:
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(categories_router, prefix="/api/v1/categories", tags=["categories"])


@app.get("/")
async def root():
    """Root endpoint - API health check."""
    return {
        "status": "healthy",
        "message": "Todo API is running",
        "version": "0.1.0",
    }


@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "0.1.0",
        "debug": settings.debug,
    }


@app.get("/api/v1/health", tags=["health"])
async def api_health_check():
    """API-specific health check for load balancers."""
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "0.1.0",
    }
