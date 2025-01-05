from fastapi import APIRouter
from controllers.vonage_controller import router as vonage_router

router = APIRouter()

router.include_router(vonage_router, prefix="/vonage", tags=["Vonage"])
