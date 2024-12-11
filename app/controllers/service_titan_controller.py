from fastapi import APIRouter, Depends
import services
from logging_module import logger
from utils.dependencies import get_current_user_id

router = APIRouter()


@router.get(
    "/get-employees",
)
async def get_service_titan_employees(page: int = 1, page_size: int = 10, user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan employees controller")
    response = await services.get_service_titan_employees(page, page_size)
    logger.debug("Response from Service Titan employees controller")
    return response


@router.get(
    "/get-customers",
)
async def get_service_titan_customers(page: int = 1, page_size: int = 10, user_id: int = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan customers controller")
    response = await services.get_service_titan_customers(page, page_size)
    logger.debug("Response from Service Titan customers controller")
    return response
