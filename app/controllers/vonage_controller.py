from fastapi import APIRouter, Request
import services
from logging_module import logger
from fastapi.responses import JSONResponse
# import background_tasks
from fastapi import BackgroundTasks

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
