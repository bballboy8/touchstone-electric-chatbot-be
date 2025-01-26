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
async def send_test_campaign_sms(to: str, text: str, user_id: str = Depends(get_current_user_id)):
    logger.debug("Inside Send Test SMS controller")
    response = await services.send_test_campaign_sms(to, text)
    logger.debug("Response from Send Test SMS controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])