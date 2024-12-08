from fastapi import APIRouter
from controllers.client_agent_training_controller import router as client_agent_training_router

router = APIRouter()

router.include_router(client_agent_training_router, prefix="/client", tags=["Client Agent Training"])
