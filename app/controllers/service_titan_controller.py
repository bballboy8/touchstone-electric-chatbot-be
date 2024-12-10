from fastapi import APIRouter
import services
from logging_module import logger

router = APIRouter()


@router.get(
    "/get-service-titan-access-token",
)
async def get_service_titan_access_token():
    logger.debug("Inside Service Titan access token controller")
    response = await services.get_service_titan_access_token()
    logger.debug("Response from Service Titan access token controller")
    return response