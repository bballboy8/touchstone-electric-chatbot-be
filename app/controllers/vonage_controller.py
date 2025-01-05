from fastapi import APIRouter
import services
from logging_module import logger
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post(
    "/send-test-sms",
)
async def send_test_sms(to: str, text: str):
    logger.debug("Inside Send Test SMS controller")
    response = await services.send_test_sms(to, text)
    logger.debug("Response from Send Test SMS controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])
