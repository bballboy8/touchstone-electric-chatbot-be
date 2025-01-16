from fastapi import APIRouter
from controllers.notion_controller import router as notion_router

router = APIRouter()

router.include_router(notion_router, prefix="/notion", tags=["Notion"])
