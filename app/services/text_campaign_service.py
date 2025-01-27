from logging_module import logger
from thirdparty.vonage_service import VonageApi
from thirdparty.service_titan_api_service import ServiceTitanApiService
from db_connection import db
from config import constants
from datetime import datetime
from datetime import timedelta
import time
import pytz
import re


async def send_test_campaign_sms(to, text):
    try:
        vonage_api = VonageApi()
        response = vonage_api.send_sms(to, text)
        if response["status_code"] != 200:
            return {"status_code": 500, "data": response["data"]}

        return {
            "status_code": 200,
            "data": f"SMS Sent Successfully to {to} with message id: {response['data']}",
        }
    except Exception as e:
        logger.error(f"Error in send_test_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}

def extract_job_info(text):
    pattern = r"Job#: (\d+).*?Technicians:\s*(\w+\s\w+)"
    match = re.search(pattern, text)
    if match:
        job_id = match.group(1)
        technician = match.group(2)
        return job_id, technician
    else:
        return None, "User"


async def send_completed_job_alert_sms(data):
    try:
        message_text = data["text"]
        if not ("completed job alert" in message_text.lower()):
            logger.error("Not a completed job alert message")
            return {"status_code": 400, "data": "Not a completed job alert message"}

        logger.debug("Processing the job completed alert message")

        job_id, technician = extract_job_info(message_text)
        if not job_id:
            logger.error("Job ID not found in the message")
            return {"status_code": 400, "data": "Job ID not found in the message"}

        logger.debug(f"Job ID: {job_id}")

        service_titan_api = ServiceTitanApiService()
        job = await service_titan_api.get_job_by_id(job_id)
        if job["status_code"] != 200:
            return {"status_code": 500, "data": job["data"]}
        job_data = job["data"]
        customer_id = job_data["customerId"]

        users_collection = db[constants.USERS_COLLECTION]
        users_message_trigger_requests_collection = db[constants.USERS_MESSAGE_TRIGGER_REQUESTS_COLLECTION]
        users_campaign_messages_collection = db[constants.USERS_CAMPAIGN_MESSAGES_COLLECTION]

        user = await users_collection.find_one({"service_titan_id": int(customer_id)})
        number, user_name = "", "User"
        if user:
            logger.error(
                "User not found in the database, get the customer ID from Service Titan"
            )
            customer_contacts = (
                await service_titan_api.get_customer_contacts_by_customer_id(
                    customer_id
                )
            )
            if customer_contacts["status_code"] != 200:
                print(customer_contacts)
                logger.error("Error in getting customer contacts from Service Titan")
                return customer_contacts
            user = customer_contacts["data"]["data"]
            for contact in user:
                if contact["type"] == "MobilePhone":
                    number = contact["value"]
                    break
                elif contact["type"] == "Phone":
                    number = contact["value"]
                    break
            customer = await service_titan_api.get_customer_by_id(customer_id)
            if customer["status_code"] != 200:
                print(customer)
                logger.error("Error in getting customer details from Service Titan")
                return customer
            customer_data = customer["data"]
            user_name = customer_data["name"]
        else:
            mobilephone = user.get("mobilephone", [])
            phone = user.get("phone", [])
            user_name = user.get("firstname", "User")
            if len(mobilephone) == 0:
                logger.error("Mobile phone number not found in the database")
            elif len(mobilephone) > 0:
                number = mobilephone[0]
            if len(phone) == 0 and not number:
                logger.error("Phone number not found in the database")
            elif len(phone) > 0 and not number:
                number = phone[0]

        if not number:
            logger.error("Phone number not found")
            return {"status_code": 500, "data": "Phone number not found"}

        message_1 = f"Hey {user_name},\nThanks for choosing Touchstone Electric!\nWould you be opposed to leaving some feedback on how {technician} did using the link below?\nhttps://g.co/kgs/odtK5fg\nIf you mention {technician} by name in a 5-star review, we will tip him on your behalf!"

        message_3 = f"Hi {user_name},\nWe hope that you're still satisfied with {technician}'s performance.\nWere there any issues regarding your experience with {technician}'s performance?"
        
        message_7 = f"Hi {user_name}. Checking in one last time.\nAre you going to be unable to give {technician} feedback on his performance?"

        for i, message in enumerate([message_1, message_3, message_7]):
            expires_at = datetime.now(pytz.utc) + timedelta(minutes=(i+1)*2)

            trigger_data = {
                "expires_at": expires_at,
                "type": "google_review",
            }
            trigger_id = await users_message_trigger_requests_collection.insert_one(trigger_data)

            user_message = {
                "trigger_id": trigger_id.inserted_id,
                "customer_id": customer_id,
                "message": message,
                "expires_at": expires_at,
                "status": "pending",
                "type": 'google_review'
            }
            await users_campaign_messages_collection.insert_one(user_message)
            logger.debug(f"Message Request Trigger added with ID: {trigger_id}")
        return {"status_code": 200, "data": f"Message Triggered with ID: {trigger_id}"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error in send_completed_job_alert_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}

async def send_text_message_via_trigger(trigger_id):
    try:
        users_campaign_messages_collection = db[constants.USERS_CAMPAIGN_MESSAGES_COLLECTION]
        user_message = await users_campaign_messages_collection.find_one({"trigger_id": trigger_id})
        if not user_message:
            return {"status_code": 404, "data": "User Message not found"}
        
        number = user_message["number"]
        message = user_message["message"]
        vonage_api = VonageApi()
        response = vonage_api.send_sms("919993227728", message, "text")
        if response["status_code"] != 200:
            await users_campaign_messages_collection.update_one({"trigger_id": trigger_id}, {"$set": {"status": "failed"}})
            return {"status_code": 500, "data": response["data"]}

        await users_campaign_messages_collection.update_one({"trigger_id": trigger_id}, {"$set": {"status": "sent"}})

        return {
            "status_code": 200,
            "data": f"SMS Sent Successfully to {number} with message id: {response['data']}",
        }
    except Exception as e:
        logger.error(f"Error in send_text_message_via_trigger: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}