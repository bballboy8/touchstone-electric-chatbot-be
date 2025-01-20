from fastapi import APIRouter
from controllers.gmail_controller import router as gmail_router

router = APIRouter()

router.include_router(gmail_router, prefix="/gmail", tags=["Gmail"])
