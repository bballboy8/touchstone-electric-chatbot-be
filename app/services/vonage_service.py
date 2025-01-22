from logging_module import logger
from thirdparty.vonage_service import VonageApi
from thirdparty.openai_service import OpenAIService
from thirdparty.pinecone_service import PineConeDBService
from db_connection import db
from config import constants
from datetime import datetime
from datetime import timedelta

async def send_test_sms(to, text):
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

async def get_users_previous_messages_history_of_last_30_days(msisdn):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        query = {"msisdn": msisdn, "created_at": {"$gte": datetime.now() - timedelta(days=30)}}
        history = await vonage_webhooks_collection.find(query).to_list(length=None)
        return {"status_code": 200, "data": list(history)}
    except Exception as e:
        logger.error(f"Error in get_users_previous_messages_history_of_last_30_days: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def inbound_sms(request):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        request['source'] = 'inbound_sms'
        request["created_at"] = datetime.now()

        vonage_api = VonageApi()
        openai_client = OpenAIService()
        pinecone_client = PineConeDBService()

        query = request["text"]

        channel = "sms"
        if "channel" in request:
            channel = request["channel"]

        to = request["msisdn"]

        response = await pinecone_client.query_data(query, 3, None)
        if response["status_code"] != 200:
            return response

        matches = response["response"]["matches"]
        context = " ".join([match["metadata"]["text"] for match in matches])

        response = await openai_client.generate_ai_agent_response(
            context=context, query=query
        )
        if response["status_code"] != 200:
            return response
        
        gpt_response = response["response"]
        request['query'] = query  
        request["response"] = gpt_response
        vonage_webhooks_collection.insert_one(request)

        if channel == "whatsapp":
            logger.info("Sending WhatsApp message")
            response = vonage_api.send_whatsapp_message(to, gpt_response)
            return response
        elif channel == "sms":
            logger.info("Sending SMS message")
            response = vonage_api.send_sms(to, gpt_response)
            return response

        logger.info("Returning from Inbound SMS service")
        return {"status_code": 200, "data": "Inbound SMS service"}
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error in inbound_sms: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}


async def sms_status(request):
    try:
        vonage_webhooks_collection = db[constants.VONAGE_WEBHOOKS_COLLECTION]
        request['source'] = 'sms_status'
        request["created_at"] = datetime.now()
        vonage_webhooks_collection.insert_one(request)
        logger.info("Inside SMS Status service")
        return {"status_code": 200, "data": "SMS Status service"}
    except Exception as e:
        logger.error(f"Error in sms_status: {e}")
        return {"status_code": 500, "data": f"Internal Server Error: {e}"}
