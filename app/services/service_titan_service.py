import os
import asyncio
import time
from concurrent.futures import ThreadPoolExecutor
from thirdparty.service_titan_api_service import ServiceTitanApiService
from logging_module import logger
from models.service_titan import ServiceTitanCustomer, ServiceTitanBookingRequest
from config import constants
from db_connection import db
from pymongo import UpdateOne


async def get_service_titan_employees(
    page: int = 1, page_size: int = 10, phone_number: str = None
):
    logger.info("Getting Service Titan employees")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_employees(page, page_size, phone_number)
        logger.info("Service Titan employees received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan employees: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def get_service_titan_customers(
    page: int = 1, page_size: int = 10, phone_number: str = None, 
):
    logger.info("Getting Service Titan customers")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_customers(page, page_size, phone_number)
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
        return {"status_code": 500, "data": f"Internal server error:{e}", "response": f"{e}"}


async def get_customer_contacts_by_customer_id(customer_id: str):
    logger.info("Getting Service Titan customer contacts by customer id")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.get_customer_contacts_by_customer_id(customer_id)
        logger.info("Service Titan customer contacts by customer id received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan customer contacts by customer id: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def fetch_data(function_call):
    try:
        response = await function_call()
        if response["status_code"] != 200:
            return response
        data = response["data"]
        all_data = data.get("data", [])
        has_more = data.get("hasMore", False)
        continue_from = data.get("continueFrom", None)

        while has_more:
            response = await function_call(continue_from)
            if response["status_code"] != 200:
                break
            data = response["data"]
            all_data.extend(data.get("data", []))
            has_more = data.get("hasMore", False)
            continue_from = data.get("continueFrom", None)
        return {"status_code": 200, "data": all_data}
    except Exception as e:
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def associate_user_contacts_threaded(user_list, contact_list, tag_list):
    users_dict = {
        user["id"]: {
            "service_titan_id": user["id"],
            "name": user["name"],
            "type": user["type"],
            "tag_id": user["tagTypeIds"],
            **user["address"],
        }
        for user in user_list
    }

    def process_contact(contact):
        customer_id = contact.get("customerId")
        if customer_id in users_dict:
            contact_type = contact.get("type", "").lower()
            contact_value = str(contact.get("value")).lower()
            if contact_value:
                if contact_type not in users_dict[customer_id]:
                    users_dict[customer_id][contact_type] = []
                users_dict[customer_id][contact_type].append(contact_value)

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(process_contact, contact_list)


    def process_tag(user_id):
        user = users_dict[user_id]
        user["tags"] = []
        for tag_id in user["tag_id"]:
            tag = next((tag for tag in tag_list if tag["id"] == tag_id), None)
            if tag:
                user["tags"].append(tag["name"])

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(process_tag, users_dict.keys())

    return list(users_dict.values())



async def export_all_customers_data_from_service_titan():
    logger.info("Exporting all customers from Service Titan")
    try:
        if constants.DEBUG:
            logger.info("Debug Mode: Skipping Export All Customers Data")
            return {"status_code": 200, "data": "Debug Mode: Skipping Export All Customers Data"}
        
        start_time = time.time()
        logger.debug("Exporting all customers from Service Titan")
        service_titan_api_service = ServiceTitanApiService()
        func_list = [
            service_titan_api_service.export_all_customers_data,
            service_titan_api_service.export_all_customers_contacts,
            service_titan_api_service.export_all_service_titan_tags
        ]

        responses = await asyncio.gather(
            fetch_data(func_list[0]),
            fetch_data(func_list[1]),
            fetch_data(func_list[2]),
        )

        response = responses[0]
        if response["status_code"] != 200:
            return response
        all_meta_data = response["data"]

        logger.info("All customers fetched from Service Titan")
        logger.info(f"Total records: {len(all_meta_data)}")

        response = responses[1]
        if response["status_code"] != 200:
            return response
        all_contacts = response["data"]
        logger.info(f"Total contacts: {len(all_contacts)}")

        response = responses[2]
        if response["status_code"] != 200:
            return response
        all_tags = response["data"]
        logger.info(f"Total tags: {len(all_tags)}")

        all_data = await associate_user_contacts_threaded(all_meta_data, all_contacts, all_tags)

        response = await seed_in_database(all_data)

        end_time = time.time()
        total_time = end_time - start_time

        logger.info(f"Time taken to export all customers from Service Titan: {total_time} seconds")
        return {
            "status_code": 200,
            "data": {
                "total_records": len(all_meta_data),
                "total_contacts": len(all_contacts),
                "aggregate_records_length": len(all_data),
                "time_taken": total_time,
                "response": response,
            },
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error exporting all customers from Service Titan: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}


async def seed_in_database(new_batch):
    try:
        # Step 1: Extract all IDs from the new batch
        users_collection = db[constants.USERS_COLLECTION]
        incoming_ids = [record["service_titan_id"] for record in new_batch]

        # Step 2: Retrieve all matching records from MongoDB in one query
        existing_records = users_collection.find({"service_titan_id": {"$in": incoming_ids}})
        existing_records_dict = {record["service_titan_id"]: record async for record in existing_records}

        # Step 3: Prepare bulk operations
        bulk_operations = []

        for record in new_batch:
            record_id = record["service_titan_id"]
            existing_record = existing_records_dict.get(record_id)

            if existing_record:
                updates = {}
                for key, value in record.items():
                    if key != "service_titan_id" and value != existing_record.get(key):
                        updates[key] = value

                if updates:
                    bulk_operations.append(
                        UpdateOne(
                            {"service_titan_id": record_id},
                            {"$set": updates}
                        )
                    )
            else:
                bulk_operations.append(
                    UpdateOne(
                        {"service_titan_id": record_id},
                        {"$setOnInsert": record},
                        upsert=True
                    )
                )

        if bulk_operations:
            result = await users_collection.bulk_write(bulk_operations)
            return (f"Matched: {result.matched_count}, Modified: {result.modified_count}, Upserts: {result.upserted_count}")
        else:
            return ("No changes detected.")
    except Exception as e:
        logger.error(f"Error seeding in database: {e}")
        return f"Internal server error: {e}"

async def get_service_titan_tags(continueFrom: str):
    logger.info("Getting Service Titan customer tags")
    try:
        service_titan_api_service = ServiceTitanApiService()
        response = await service_titan_api_service.export_all_service_titan_tags(continueFrom)
        logger.info("Service Titan customer tags received")
        if response["status_code"] != 200:
            return response
        return {"status_code": 200, "data": response["data"]}
    except Exception as e:
        logger.error(f"Error getting Service Titan customer tags: {e}")
        return {"status_code": 500, "data": f"Internal server error:{e}"}