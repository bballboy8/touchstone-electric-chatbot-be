from fastapi import APIRouter
import services
import schemas
from logging_module import logger

router = APIRouter()


@router.get(
    "/openai",
    response_description="Health check for OpenAI service",
    responses=schemas.openai_health_check_response_schema
)
async def openai_health_check():
    logger.debug("Inside OpenAI health check controller")
    response = await services.test_openai_service()
    logger.debug("Response from OpenAI health check service")
    return response

