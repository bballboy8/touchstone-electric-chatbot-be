from fastapi import APIRouter
from controllers.email_agent_controller import router as email_agent_router

router = APIRouter()

router.include_router(email_agent_router, prefix="/email", tags=["Email Agent"])
