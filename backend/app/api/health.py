from fastapi import APIRouter
from datetime import datetime
from typing import Dict

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=Dict)
async def health_check():
    """Health check endpoint to verify API service availability"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }