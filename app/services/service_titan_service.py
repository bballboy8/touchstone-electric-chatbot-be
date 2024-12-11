from thirdparty.service_titan_api_service import ServiceTitanApiService
from logging_module import logger
from utils.dependencies import get_current_user_id
from fastapi import Depends


async def get_service_titan_employees(
    page: int = 1, page_size: int = 10
):
    logger.info("Getting Service Titan employees")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_employees(page, page_size)
        logger.info("Service Titan employees received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan employees: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def get_service_titan_customers(
    page: int = 1, page_size: int = 10
):
    logger.info("Getting Service Titan customers")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_customers(page, page_size)
        logger.info("Service Titan customers received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan customers: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}
