from fastapi import APIRouter, Request
import services
from logging_module import logger
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get(
    "/get-team-contact-list",
)
async def get_team_contact_list():
    logger.debug("Get Team Contact List controller")
    response = await services.get_formatted_team_contacts()
    logger.debug(f"Returning from Get Team Contact List controller")
    return JSONResponse(status_code=response["status_code"], content=response["data"])
