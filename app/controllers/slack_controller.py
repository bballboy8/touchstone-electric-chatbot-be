from fastapi import APIRouter, Depends, Request, BackgroundTasks
import services
from logging_module import logger
from services import slack_service
from fastapi.responses import JSONResponse
from utils.dependencies import get_current_user_id


router = APIRouter()


existing_signatures = []

@router.post("/events")
async def slack_events_handler(request: Request, background_tasks: BackgroundTasks):
    headers = request.headers
    if  headers.get("x-slack-signature") in existing_signatures:
        if len(existing_signatures) > 10:
            existing_signatures.pop(0)
        return JSONResponse(content={"status": "ok"}, status_code=200)
    
    existing_signatures.append(headers.get("x-slack-signature"))

    logger.debug("Inside Slack events handler controller")
    body = await request.body()


    if headers.get("content-type") == "application/json":
        data = await request.json()
    elif headers.get("content-type") == "application/x-www-form-urlencoded":
        data = await request.form()
    else:
        logger.error("Invalid content type")
        return JSONResponse(content={"status": "error"}, status_code=400)
    
    event_type = data["event"]["type"]
    if event_type == "app_mention":
        background_tasks.add_task(
            slack_service.slack_events_handler, data, body, headers
        )

    if data["type"] == "url_verification":
        return JSONResponse(content={"challenge": data["challenge"]}, status_code=200)

    logger.debug("Response from Slack events handler controller")
    return JSONResponse(content={"status": "ok"}, status_code=200)

@router.get("/get-slack-channel-list")
async def get_slack_channel_list(cursor: str = None, user_id = Depends(get_current_user_id)):
    logger.debug("Inside get slack channel list controller")
    response = await slack_service.get_slack_channel_list(cursor)
    return JSONResponse(content=response, status_code=200)
