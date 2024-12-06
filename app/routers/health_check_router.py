from fastapi import APIRouter
from controllers.health_check_controller import router as health_check_router

router = APIRouter()

router.include_router(health_check_router, prefix="/healthcheck", tags=["Health Check"])
