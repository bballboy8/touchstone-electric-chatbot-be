from fastapi import APIRouter, Request, Depends
import services
from logging_module import logger
from fastapi.responses import JSONResponse
from utils.dependencies import get_current_user_id

router = APIRouter()


@router.get(
    "/get-team-contact-list",
)
async def get_team_contact_list(user_id = Depends(get_current_user_id)):
    logger.debug("Get Team Contact List controller")
    response = await services.get_formatted_team_contacts()
    logger.debug(f"Returning from Get Team Contact List controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])
