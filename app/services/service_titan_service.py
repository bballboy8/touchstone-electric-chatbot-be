from thirdparty.service_titan_api_service import ServiceTitanApiService
from logging_module import logger
from models.service_titan import ServiceTitanCustomer, ServiceTitanBookingRequest


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


async def get_service_titan_jobs(page: int = 1, page_size: int = 10):
    logger.info("Getting Service Titan jobs")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_jobs(page, page_size)
        logger.info("Service Titan jobs received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan jobs: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def get_service_titan_job_by_id(job_id: int):
    logger.info("Getting Service Titan job by id")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_job_by_id(job_id)
        logger.info("Service Titan job by id received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan job by id: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def get_service_titan_locations(page: int = 1, page_size: int = 10):
    logger.info("Getting Service Titan locations")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_locations(page, page_size)
        logger.info("Service Titan locations received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan locations: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def get_service_titan_location_by_id(location_id: int):
    logger.info("Getting Service Titan location by id")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_location_by_id(location_id)
        logger.info("Service Titan location by id received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan location by id: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}
    
async def create_service_titan_customer(customer_data: ServiceTitanCustomer):
    logger.info("Creating Service Titan customer")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.create_customer(customer_data)
        if response["status_code"] != 200:
            return response
        logger.info("Service Titan customer created")
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error creating Service Titan customer: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}
    
async def get_customer_by_id(customer_id: int):
    logger.info("Getting Service Titan customer by id")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_customer_by_id(customer_id)
        logger.info("Service Titan customer by id received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan customer by id: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}
    
async def create_booking_request(booking_data: ServiceTitanBookingRequest, conversation_summary: str = None):
    logger.info("Creating Service Titan booking request")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.create_booking(booking_data, conversation_summary)
        if response["status_code"] != 200:
            return response
        logger.info("Service Titan booking request created")
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error creating Service Titan booking request: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}

    