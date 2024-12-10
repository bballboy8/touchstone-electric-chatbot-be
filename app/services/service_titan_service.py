from thirdparty.service_titan_api_service import ServiceTitanApiService
from logging_module import logger


async def get_service_titan_access_token():
    logger.info("Getting Service Titan access token")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = service_titan_api_service.get_access_token()
        logger.info("Service Titan access token received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]["access_token"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan access token: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}
