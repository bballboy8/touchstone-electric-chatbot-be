from fastapi import APIRouter, Depends, Request, BackgroundTasks
import services
from logging_module import logger
from services import slack_service
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/events")
async def slack_events_handler(request: Request, background_tasks: BackgroundTasks):
    is_duplicate = slack_service.is_duplicate_request(headers)
    if is_duplicate:
        return JSONResponse(content={"status": "ok"}, status_code=200)
    logger.debug("Inside Slack events handler controller")
    body = await request.body()
    headers = request.headers

    if headers.get("Content-Type") == "application/json":
        data = await request.json()
    elif headers.get("Content-Type") == "application/x-www-form-urlencoded":
        data = await request.form()
    else:
        logger.error("Invalid content type")
        return JSONResponse(content={"status": "error"}, status_code=400)
    background_tasks.add_task(
        slack_service.slack_events_handler, data, body, headers
    )

    if data["type"] == "url_verification":
        return JSONResponse(content={"challenge": data["challenge"]}, status_code=200)

    logger.debug("Response from Slack events handler controller")
    return JSONResponse(content={"status": "ok"}, status_code=200)
