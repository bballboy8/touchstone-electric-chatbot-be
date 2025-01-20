from fastapi import APIRouter
import services
from logging_module import logger
from fastapi import Form
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post(
    "/process-email-agent-query"
)
async def process_email_agent_query(query: str):
    logger.debug("Inside Process Email Agent Query controller")
    response = await services.process_email_agent_query_service(query)
    logger.debug("Response from Process Email Agent Query controller")
    return JSONResponse(content=response, status_code=200)