from fastapi import APIRouter
import services
from logging_module import logger
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post(
    "/get-unread-emails"
)
async def get_unread_emails():
    logger.debug("Inside Get Unread Emails controller")
    response = await services.get_unread_emails_service()
    logger.debug("Response from Get Unread Emails controller")
    return JSONResponse(content=response, status_code=200)

@router.post(
    "/get-unread-emails-with-threads"
)
async def get_unread_emails_with_threads():
    logger.debug("Inside Get Unread Emails with Threads controller")
    response = await services.get_unread_emails_with_threads()
    logger.debug("Response from Get Unread Emails with Threads controller")
    return JSONResponse(content=response, status_code=200)