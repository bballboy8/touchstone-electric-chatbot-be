from fastapi import APIRouter
from controllers.pincone_controller import router as pinecone_router

router = APIRouter()

router.include_router(pinecone_router, prefix="/pinecone", tags=["Pinecone"])
