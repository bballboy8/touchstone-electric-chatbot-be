from fastapi import APIRouter
from controllers.text_campaign_controller import router as text_campaign_router

router = APIRouter()

router.include_router(text_campaign_router, prefix="/campaign", tags=["Text Campaign"])
