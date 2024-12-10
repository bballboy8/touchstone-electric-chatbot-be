from fastapi import APIRouter
from controllers.service_titan_controller import router as service_titan_router

router = APIRouter()

router.include_router(service_titan_router, prefix="/service-titan", tags=["Service Titan"])
