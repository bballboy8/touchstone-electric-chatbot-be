from fastapi import APIRouter, Request, Depends
import services
from logging_module import logger
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks
from utils.dependencies import get_current_user_id

router = APIRouter()


@router.post(
    "/send-test-sms",
)
async def send_test_sms(to: str, text: str):
    logger.debug("Inside Send Test SMS controller")
    response = await services.send_test_sms(to, text)
    logger.debug("Response from Send Test SMS controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])


@router.post(
    "/inbound-sms",
)
async def inbound_sms(request: Request, background_tasks: BackgroundTasks):
    logger.debug("Inside Inbound SMS controller")
    request = await request.json()
    background_tasks.add_task(services.inbound_sms, request)
    logger.debug("Response from Inbound SMS controller")
    return JSONResponse(status_code=200, content="Message received")


@router.post(
    "/sms-status",
)
async def sms_status(request: Request, background_tasks: BackgroundTasks):
    logger.debug("Inside SMS Status controller")
    request = await request.json()
    background_tasks.add_task(services.sms_status, request)
    logger.debug("Response from SMS Status controller")
    return JSONResponse(status_code=200, content="Status received")


@router.get(
    "/get-users-previous-messages-history-of-last-30-days",
)
async def get_users_previous_messages_history_of_last_30_days(msisdn: str, recent_filter: bool):
    logger.debug("Inside Get Users Previous Messages History of Last 30 Days controller")
    response = await services.get_users_previous_messages_history_of_last_30_days(msisdn,recent_filter)
    logger.debug("Response from Get Users Previous Messages History of Last 30 Days controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])

@router.get(
    "/get-server-time",
)
async def get_server_time(user_id = Depends(get_current_user_id)):
    logger.debug("Inside Get Server Time controller")
    response = await services.get_server_time()
    logger.debug("Response from Get Server Time controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])

@router.get(
    '/get-users-details-in-a-text-chunk-from-db',
)
async def get_users_details_in_a_text_chunk_from_db(number: int, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Get Users Details in a Text Chunk from DB controller")
    response = await services.get_users_details_in_a_text_chunk_from_db(number)
    logger.debug("Response from Get Users Details in a Text Chunk from DB controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])