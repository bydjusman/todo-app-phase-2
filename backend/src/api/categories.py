from fastapi import APIRouter
from src.api.tasks import router as tasks_router

# Hum sirf router ko export kar rahe hain taake main.py ko mil jaye
router = tasks_router