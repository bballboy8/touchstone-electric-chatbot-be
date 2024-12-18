from fastapi import APIRouter
from controllers.slack_controller import router as slack_router

router = APIRouter()

router.include_router(slack_router, prefix="/slack", tags=["Slack"])
