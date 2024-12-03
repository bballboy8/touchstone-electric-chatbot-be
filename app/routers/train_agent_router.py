from fastapi import APIRouter
from controllers.train_agent_controller import router as train_agent_router

router = APIRouter()

router.include_router(train_agent_router, prefix="/train-agent", tags=["Train Agent"])
