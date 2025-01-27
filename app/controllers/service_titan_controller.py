from fastapi import APIRouter, Depends
import services
from logging_module import logger
from utils.dependencies import get_current_user_id
from models.service_titan import ServiceTitanCustomer, ServiceTitanBookingRequest

router = APIRouter()


@router.get(
    "/get-employees",
)
async def get_service_titan_employees(
    page: int = 1,
    page_size: int = 10,
    phone_number: str = None,
    user_id=Depends(get_current_user_id),
):
    logger.debug("Inside Service Titan employees controller")
    response = await services.get_service_titan_employees(page, page_size, phone_number)
    logger.debug("Response from Service Titan employees controller")
    return response


@router.get(
    "/get-customers",
)
async def get_service_titan_customers(
    page: int = 1,
    page_size: int = 10,
    phone_number: str = None,
    user_id=Depends(get_current_user_id),
):
    logger.debug("Inside Service Titan customers controller")
    response = await services.get_service_titan_customers(page, page_size, phone_number)
    logger.debug("Response from Service Titan customers controller")
    return response


@router.get(
    "/get-jobs",
)
async def get_service_titan_jobs(page: int = 1, page_size: int = 10, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan jobs controller")
    response = await services.get_service_titan_jobs(page, page_size)
    logger.debug("Response from Service Titan jobs controller")
    return response


@router.get(
    "/get-job-by-id",
)
async def get_service_titan_job_by_id(job_id: int, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan job by id controller")
    response = await services.get_service_titan_job_by_id(job_id)
    logger.debug("Response from Service Titan job by id controller")
    return response


@router.get(
    "/get-locations",
)
async def get_service_titan_locations(page: int = 1, page_size: int = 10, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan locations controller")
    response = await services.get_service_titan_locations(page, page_size)
    logger.debug("Response from Service Titan locations controller")
    return response


@router.get(
    "/get-location-by-id",
)
async def get_service_titan_location_by_id(location_id: int, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan location by id controller")
    response = await services.get_service_titan_location_by_id(location_id)
    logger.debug("Response from Service Titan location by id controller")
    return response

@router.post(
    "/create-customer",
)
async def create_service_titan_customer(customer_data: ServiceTitanCustomer, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan create customer controller")
    response = await services.create_service_titan_customer(customer_data)
    logger.debug("Response from Service Titan create customer controller")
    return response

@router.get(
    "/get-customer-by-id",
)
async def get_service_titan_customer_by_id(customer_id: int, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan customer by id controller")
    response = await services.get_customer_by_id(customer_id)
    logger.debug("Response from Service Titan customer by id controller")
    return response

@router.post(
    "/create-booking",
)
async def create_service_titan_booking(booking_data: ServiceTitanBookingRequest, user_id = Depends(get_current_user_id)):
    logger.debug("Inside Service Titan create booking controller")
    response = await services.create_booking_request(booking_data)
    logger.debug("Response from Service Titan create booking controller")
    return response


@router.get(
    "/get-customer-contacts",
)
async def get_service_titan_customer_contacts(
    customer_id: str,
    user_id = Depends(get_current_user_id),
):
    logger.debug("Inside Service Titan customer contacts controller")
    response = await services.get_customer_contacts_by_customer_id(customer_id)
    logger.debug("Response from Service Titan customer contacts controller")
    return response


@router.get(
    "/export-all-customers-data"
)
async def export_all_customers_data(user_id = Depends(get_current_user_id)):
    logger.debug("Inside export all customers data controller")
    response = await services.export_all_customers_data_from_service_titan()
    logger.debug("Response from export all customers data controller")
    return response


@router.get(
    "/get-service-titan-tags"
)
async def get_service_titan_tags(continueFrom:str = None, user_id = Depends(get_current_user_id)):
    logger.debug("Inside get service titan tags controller")
    response = await services.get_service_titan_tags(continueFrom)
    logger.debug("Response from get service titan tags controller")
    return response